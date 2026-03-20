"""FastAPI application -- language feedback endpoint."""

import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from google import genai
from google.genai import types
from app.feedback import get_feedback
from app.models import FeedbackRequest, FeedbackResponse

load_dotenv()

app = FastAPI(
    title="Language Feedback API",
    description="Analyzes learner-written sentences and provides structured language feedback.",
    version="1.0.0",
)
client = genai.Client(api_key=os.environ.get("GENAI_API_KEY"))

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/feedback", response_model=FeedbackResponse)
async def feedback(request: FeedbackRequest) -> FeedbackResponse:
    return await get_feedback(request)
