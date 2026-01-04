"""
FastAPI Backend for Hugging Face Space Deployment
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid

from app.config import settings
from app.models import ChatRequest, ChatResponse, Citation

# Check if running on Hugging Face
IS_HF = os.getenv("SPACE_ID") is not None or os.getenv("GRADIO") is not None

# Initialize FastAPI app
app = FastAPI(
    title="Physical AI Chatbot API",
    version="1.0.0",
    description="RAG-powered chatbot for Physical AI course"
)

# CORS middleware - allow all origins (needed for Hugging Face)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import services based on environment
print(f"Mode: {'HUGGING FACE' if IS_HF else 'LOCAL'}")

if IS_HF:
    # Hugging Face - Use Groq
    if settings.GROQ_API_KEY:
        print("Using Groq AI (Llama 3.3)")
        from app.groq_service import GroqService as AIService
    elif settings.OPENAI_API_KEY:
        print("Using OpenAI")
        from app.openai_service import OpenAIService as AIService
    else:
        print("No AI service configured")
        from app.test_mode import MockOpenAIService as AIService

    from app.qdrant_service import QdrantService

    ai_service = AIService()
    qdrant_service = QdrantService()
else:
    # Local - Test mode fallback
    print("LOCAL MODE: Using test mode")
    from app.test_mode import MockOpenAIService as AIService
    from app.test_mode import MockQdrantService as QdrantService

    ai_service = AIService()
    qdrant_service = QdrantService()


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Physical AI Chatbot API - Hugging Face",
        "version": "1.0.0",
        "mode": "HUGGING FACE" if IS_HF else "LOCAL",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "mode": "HUGGING FACE" if IS_HF else "LOCAL",
        "groq_configured": bool(settings.GROQ_API_KEY),
        "openai_configured": bool(settings.OPENAI_API_KEY),
        "qdrant_configured": bool(settings.QDRANT_URL)
    }


@app.post("/api/chat/query", response_model=ChatResponse)
async def chat_query(request: ChatRequest):
    """
    Main chat endpoint with RAG

    Workflow:
    1. Generate embedding for user query
    2. Search Qdrant for relevant context
    3. Build prompt with context
    4. Generate response with Groq
    5. Extract citations
    6. Return response
    """
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())

        # Step 1: Generate query embedding
        query_text = request.message
        if request.context:
            query_text = f"{request.context}\n\nQuestion: {request.message}"

        print(f"Generating embedding for: {query_text[:50]}...")
        query_embedding = await ai_service.generate_embedding(query_text)

        # Step 2: Search Qdrant for relevant context
        print(f"Searching Qdrant (top_k={settings.TOP_K_RESULTS})...")
        similar_docs = await qdrant_service.search_similar(
            query_embedding=query_embedding,
            top_k=settings.TOP_K_RESULTS
        )

        print(f"Found {len(similar_docs)} relevant documents")

        # Step 3: Generate response with context
        print("Generating AI response...")
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

        return ChatResponse(
            response=response_text,
            citations=citations,
            session_id=session_id
        )

    except Exception as e:
        print(f"Error in chat_query: {e}")
        raise e


@app.get("/api/chat/history/{session_id}")
async def get_chat_history(session_id: str):
    """Get conversation history for a session"""
    try:
        if not IS_HF:
            return {
                "session_id": session_id,
                "messages": [],
                "note": "Hugging Face deployment - history not stored"
            }

        from app.database import get_database, Conversation
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
        print(f"Error in get_chat_history: {e}")
        raise e


@app.get("/api/collection/info")
async def get_collection_info():
    """Get Qdrant collection information"""
    try:
        info = await qdrant_service.get_collection_info()
        return info
    except Exception as e:
        print(f"Error getting collection info: {e}")
        raise e


@app.post("/api/collection/create")
async def create_collection():
    """Create Qdrant collection (admin endpoint)"""
    try:
        await qdrant_service.create_collection()
        return {"message": "Collection created successfully"}
    except Exception as e:
        print(f"Error creating collection: {e}")
        raise e


if __name__ == "__main__":
    import uvicorn

    if IS_HF:
        # Hugging Face - use port 7860
        uvicorn.run("app:app", host="0.0.0.0", port=7860)
    else:
        # Local - use port 8000
        uvicorn.run("app:app", host="0.0.0.0", port=8000)
