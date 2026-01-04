"""
FastAPI Backend for Physical AI Chatbot with RAG
Supports both production and test modes
"""

import uuid
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.models import ChatRequest, ChatResponse, Citation

# Check if test mode
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"

if TEST_MODE:
    print("TEST MODE: Running with mock responses")
    from app.test_mode import MockOpenAIService as AIService
    from app.test_mode import MockQdrantService as QdrantService
else:
    print("PRODUCTION MODE: Running with real APIs")
    # Use Groq if available, otherwise fallback to OpenAI
    if settings.GROQ_API_KEY:
        print("Using Groq AI (Llama 3.1)")
        from app.groq_service import GroqService as AIService
    elif settings.OPENAI_API_KEY:
        print("Using OpenAI")
        from app.openai_service import OpenAIService as AIService
    else:
        print("No AI service configured, falling back to test mode")
        TEST_MODE = True
        from app.test_mode import MockOpenAIService as AIService

    from app.qdrant_service import QdrantService

from app.database import get_database, Conversation

# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="RAG-powered chatbot for Physical AI & Humanoid Robotics textbook"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS + ["*"],  # Allow all in test mode
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
ai_service = AIService()
qdrant_service = QdrantService()


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Physical AI Chatbot API",
        "version": settings.API_VERSION,
        "mode": "TEST" if TEST_MODE else "PRODUCTION",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.API_VERSION,
        "mode": "TEST" if TEST_MODE else "PRODUCTION",
        "ai_service": "Groq" if settings.GROQ_API_KEY else ("OpenAI" if settings.OPENAI_API_KEY else "None"),
        "groq_configured": bool(settings.GROQ_API_KEY),
        "openai_configured": bool(settings.OPENAI_API_KEY),
        "qdrant_configured": bool(settings.QDRANT_URL),
        "database_configured": bool(settings.DATABASE_URL)
    }


@app.post("/api/chat/query", response_model=ChatResponse)
async def chat_query(request: ChatRequest):
    """
    Main chat endpoint with RAG

    Workflow:
    1. Generate embedding for user query
    2. Search Qdrant for relevant context
    3. Build prompt with context
    4. Generate response with OpenAI
    5. Extract citations
    6. Save conversation to database
    """
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())

        # Step 1: Generate query embedding
        query_text = request.message
        if request.context:
            query_text = f"{request.context}\n\nQuestion: {request.message}"

        query_embedding = await ai_service.generate_embedding(query_text)

        # Step 2: Search Qdrant for relevant context
        similar_docs = await qdrant_service.search_similar(
            query_embedding=query_embedding,
            top_k=settings.TOP_K_RESULTS
        )

        # Step 3: Generate response with context
        response_text = await ai_service.generate_chat_response(
            user_message=request.message,
            context_documents=similar_docs
        )

        # Step 4: Build citations
        citations = [
            Citation(
                chapter=doc["chapter"],
                section=doc["section"],
                url=doc["url"],
                relevance_score=doc["score"]
            )
            for doc in similar_docs[:3]  # Top 3 citations
        ]

        # Step 5: Save to database (optional)
        if not TEST_MODE:
            try:
                db = get_database()
                if db:
                    conversation = Conversation(
                        session_id=session_id,
                        user_message=request.message,
                        ai_response=response_text,
                        context=request.context
                    )
                    db.add(conversation)
                    db.commit()
                    db.close()
            except Exception as db_error:
                print(f"Database error (non-critical): {db_error}")

        return ChatResponse(
            response=response_text,
            citations=citations,
            session_id=session_id
        )

    except Exception as e:
        print(f"Error in chat_query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/chat/history/{session_id}")
async def get_chat_history(session_id: str):
    """Get conversation history for a session"""
    try:
        if TEST_MODE:
            return {
                "session_id": session_id,
                "messages": [],
                "note": "Test mode - history not saved"
            }

        db = get_database()
        if not db:
            return {"session_id": session_id, "messages": []}

        conversations = db.query(Conversation).filter(
            Conversation.session_id == session_id
        ).order_by(Conversation.created_at).all()

        messages = [
            {
                "user_message": conv.user_message,
                "ai_response": conv.ai_response,
                "created_at": conv.created_at.isoformat()
            }
            for conv in conversations
        ]

        db.close()

        return {
            "session_id": session_id,
            "messages": messages
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/collection/info")
async def get_collection_info():
    """Get Qdrant collection information"""
    try:
        info = await qdrant_service.get_collection_info()
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/collection/create")
async def create_collection():
    """Create Qdrant collection (admin endpoint)"""
    try:
        await qdrant_service.create_collection()
        return {"message": "Collection created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
