import os

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from transformers import pipeline
from dotenv import load_dotenv


class TextItem(BaseModel):
    text: str


class TextItemList(BaseModel):
    texts: List[str]


# Load environment variables
load_dotenv()

model = os.getenv("MODEL_NAME")

app = FastAPI()

sentiment_analysis = pipeline("sentiment-analysis", model=model, truncation=True)


@app.post("/predict/")
async def predict_sentiment(text_item: TextItem):
    zero_shot_prompt = f"Decide whether the sentiment of the input sentence is positive or negative: {text_item.text}"
    response = sentiment_analysis(zero_shot_prompt)
    return response[0]


# Run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
