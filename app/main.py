"""FastAPI application -- language feedback endpoint."""

import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import json
import app.models
import app.feedback

load_dotenv()

application = FastAPI(
    title="Language Feedback API",
    description="Analyzes learner-written sentences and provides structured language feedback.",
    version="1.0.0",
)

@application.get("/health")
async def health():
    return {"status": "ok"}


@application.post("/feedback", response_model=app.models.FeedbackResponse)
async def feedback(request: app.models.FeedbackRequest) -> app.models.FeedbackResponse:
    try:
        return await app.feedback.get_feedback(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing feedback: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(application, host="0.0.0.0", port=8000)