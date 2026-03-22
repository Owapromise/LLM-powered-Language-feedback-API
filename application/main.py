"""FastAPI application -- language feedback endpoint."""

import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from application.models import FeedbackRequest, FeedbackResponse
from application.feedback import get_feedback
load_dotenv()

app = FastAPI(
    title="Language Feedback API",
    description="Analyzes learner-written sentences and provides structured language feedback.",
    version="1.0.0",
)

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/feedback", response_model=FeedbackResponse)
async def feedback(request: FeedbackRequest) -> FeedbackResponse:
    try:
        return await get_feedback(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing feedback: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)