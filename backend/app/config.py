"""
Configuration management using environment variables
"""

import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment"""

    # API Info
    API_TITLE: str = "Physical AI Chatbot API"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = False
    TEST_MODE: bool = False

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]

    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    OPENAI_MAX_TOKENS: int = 1500
    OPENAI_TEMPERATURE: float = 0.7

    # Groq
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # Gemini
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-flash"

    # Qdrant
    QDRANT_URL: str = ""
    QDRANT_API_KEY: str = ""
    QDRANT_COLLECTION_NAME: str = "physical_ai_textbook"
    QDRANT_VECTOR_SIZE: int = 384  # sentence-transformers all-MiniLM-L6-v2 uses 384 dimensions

    # Neon Postgres
    DATABASE_URL: str = ""

    # RAG Settings
    TOP_K_RESULTS: int = 5
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
