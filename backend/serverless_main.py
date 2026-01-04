"""
Vercel-compatible FastAPI entry point for serverless deployment
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.config import settings
from app.models import ChatRequest, ChatResponse, Citation
import uuid

# Initialize FastAPI app
app = FastAPI(
    title="Physical AI Chatbot API",
    version="1.0.0"
)

# CORS middleware - allow all origins for serverless
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Check if running on Vercel (serverless)
IS_VERCEL = os.getenv("VERCEL", "false").lower() == "true"

# Import services based on environment
if not IS_VERCEL:
    # Local development - use full backend
    print("LOCAL MODE: Using full backend")
    TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"

    if TEST_MODE:
        print("TEST MODE: Running with mock responses")
        from app.test_mode import MockOpenAIService as AIService
        from app.test_mode import MockQdrantService as QdrantService
    else:
        print("PRODUCTION MODE: Running with real APIs")
        # Use Groq if available, otherwise fallback to OpenAI
        if settings.GROQ_API_KEY:
            print("Using Groq AI (Llama 3.3)")
            from app.groq_service import GroqService as AIService
        elif settings.OPENAI_API_KEY:
            print("Using OpenAI")
            from app.openai_service import OpenAIService as AIService
        else:
            print("No AI service configured, falling back to test mode")
            from app.test_mode import MockOpenAIService as AIService

        from app.qdrant_service import QdrantService

    ai_service = AIService()
    qdrant_service = QdrantService()

else:
    # Vercel serverless - simple mock response for now
    print("VERCEL MODE: Using simplified backend")

    @app.get("/")
    async def root():
        return {
            "message": "Physical AI Chatbot API",
            "version": "1.0.0",
            "mode": "VERCEL",
            "health": "/health"
        }

    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "version": "1.0.0",
            "mode": "VERCEL",
            "note": "Backend deployed on Vercel serverless"
        }

    @app.post("/api/chat/query", response_model=ChatResponse)
    async def chat_query(request: ChatRequest):
        """
        Simplified chat endpoint for Vercel serverless
        """
        try:
            # Generate session ID
            session_id = request.session_id or str(uuid.uuid4())

            # Simple response for now (will connect to real backend later)
            from app.groq_service import GroqService
            ai = GroqService()

            # Simple context-free response
            response = await ai.generate_chat_response(
                user_message=request.message,
                context_documents=[]
            )

            return ChatResponse(
                response=response,
                citations=[],
                session_id=session_id
            )

        except Exception as e:
            print(f"Error: {e}")
            return ChatResponse(
                response="Sorry, the chatbot is experiencing some issues. This is a simplified version for Vercel deployment. Please check back soon!",
                citations=[],
                session_id=str(uuid.uuid4())
            )
