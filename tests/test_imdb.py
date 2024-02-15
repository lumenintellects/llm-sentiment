import os
import requests
import pandas as pd
from dotenv import load_dotenv
import mlflow
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.preprocessing import LabelEncoder
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load environment variables
load_dotenv()

# MLflow setup
mlflow.set_tracking_uri(os.getenv("MLFLOW_URL"))
mlflow.set_experiment("Sentiment_Analysis_IMDb_Evaluation")
url = os.getenv("PREDICT_URL") + "/predict/"  # Endpoint for individual predictions

# Load and preprocess the IMDb dataset
df = pd.read_csv('data/IMDB_dataset.csv')
df['sentiment'] = df['sentiment'].map({'positive': 'POSITIVE', 'negative': 'NEGATIVE'}).astype('category')


def send_prediction_request(text):
    try:
        response = requests.post(url, json={"text": text})
        response.raise_for_status()
        return response.json()['label']
    except requests.exceptions.RequestException as err:
        print(f"Error during prediction request: {err}")
        return None


def predict_sentiments_parallel(texts, max_workers=20):
    predictions = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_text = {executor.submit(send_prediction_request, text): text for text in texts}
        for future in as_completed(future_to_text):
            prediction = future.result()
            if prediction is not None:
                predictions.append(prediction)
            else:
                # Handle None predictions if necessary
                predictions.append('UNKNOWN')
    return predictions


def evaluate_model_parallel(texts, labels):
    predictions = predict_sentiments_parallel(texts)

    # Encode labels for metric calculation
    le = LabelEncoder()
    labels_encoded = le.fit_transform(labels)
    predictions_encoded = le.transform(predictions)

    with mlflow.start_run(run_name="Model Evaluation"):
        precision = precision_score(labels_encoded, predictions_encoded, average='weighted', zero_division=0)
        recall = recall_score(labels_encoded, predictions_encoded, average='weighted', zero_division=0)
        f1 = f1_score(labels_encoded, predictions_encoded, average='weighted', zero_division=0)

        mlflow.log_metrics({"Precision": precision, "Recall": recall, "F1 Score": f1})


# Split dataset for evaluation
texts = df['review'].tolist()[:50]
labels = df['sentiment'].tolist()[:50]

# Evaluate the model on a larger dataset using parallel processing
evaluate_model_parallel(texts, labels)
