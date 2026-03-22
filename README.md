# LLM-Powered Language Feedback API

## Overview
This repository contains a FastAPI-based backend that acts as an AI-powered language learning assistant. It receives learner-written sentences, analyzes them for errors across multiple categories (grammar, spelling, word choice, etc.), and provides structured, friendly feedback using OpenAI's `gpt-4o-mini` model.

## Design Decisions

### Framework Choice: FastAPI & Pydantic
I chose FastAPI because it is extremely fast, fully supports asynchronous Python (essential for non-blocking LLM API calls), and integrates seamlessly with Pydantic. Pydantic is used to strongly type the `FeedbackRequest` and `FeedbackResponse` schemas, ensuring that no invalid data enters or leaves the API.

### Model Choice: OpenAI `gpt-4o-mini`
For a production API, latency and cost are critical. `gpt-4o-mini` provides near-instantaneous responses and costs a fraction of larger models, while still possessing excellent multilingual capabilities and strict adherence to JSON schemas. 

### Production Feasibility
- **Token Efficiency:** The system prompt is kept concise, and instructions are clearly numbered to reduce token overhead.
- **Reliability:** By using OpenAI's `response_format={"type": "json_object"}`, the API guarantees valid JSON output, eliminating parsing crashes. 
- **Asynchronous Processing:** Utilizing the `AsyncOpenAI` client prevents the server from blocking while waiting for external API responses, allowing it to scale and handle multiple concurrent users.

## Prompt Strategy
The prompt was engineered to prioritize accurate, schema-compliant, and educational output:
1. **Role Definition:** The LLM is primed as a "language-learning assistant" to ensure explanations are encouraging and friendly.
2. **Explicit Edge Cases:** Rule #1 explicitly dictates how to handle perfectly correct sentences (returning `is_correct=true` and an empty array) to avoid hallucinated corrections.
3. **Native Language Explanations:** The prompt instructs the model to explain errors in the learner's native language, reducing cognitive load for the student.
4. **Schema Enforcement:** The required JSON structure is provided directly in the prompt, guiding the model's output parser.

## How to Run

### Prerequisites
- Docker & Docker Compose
- An OpenAI API Key

### Setup
1. Create your environment file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and add your API key:
   ```
   OPENAI_API_KEY=your_actual_key_here
   ```

### Run with Docker (Recommended)
Build and start the container using Docker Compose:
```bash
docker compose up --build
```
The API will be available at `http://localhost:8000`. You can test the endpoints interactively via the Swagger UI at `http://localhost:8000/docs`.

### Run Locally (Without Docker)
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Testing
The project includes a robust test suite covering schema compliance, mocked unit tests, and live integration tests across multiple languages (including non-Latin scripts like Japanese).

```bash
# Run unit and schema validation tests (no API key needed)
pytest tests/test_feedback_unit.py tests/test_schema.py -v

# Run live integration tests (requires OPENAI_API_KEY)
pytest tests/test_feedback_integration.py -v
```
