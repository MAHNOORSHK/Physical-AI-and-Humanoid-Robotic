# Backend - RAG Chatbot API

FastAPI backend with OpenAI, Qdrant, and Neon Postgres.

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

API will be available at: http://localhost:8000

## Environment

Copy `.env.example` to `.env` and add your API keys.
