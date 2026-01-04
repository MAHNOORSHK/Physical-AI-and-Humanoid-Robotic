"""
Pydantic models for request/response
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class Citation(BaseModel):
    """Citation for source reference"""
    chapter: str
    section: str
    url: str
    relevance_score: Optional[float] = None


class ChatRequest(BaseModel):
    """Chat request from user"""
    message: str = Field(..., min_length=1, max_length=5000)
    session_id: Optional[str] = None
    context: Optional[str] = None  # Selected text

    class Config:
        json_schema_extra = {
            "example": {
                "message": "What is ROS 2?",
                "session_id": "session_123",
                "context": "ROS 2 is the Robot Operating System..."
            }
        }


class ChatResponse(BaseModel):
    """Chat response with citations"""
    response: str
    citations: List[Citation] = []
    session_id: str

    class Config:
        json_schema_extra = {
            "example": {
                "response": "ROS 2 is a middleware framework...",
                "citations": [
                    {
                        "chapter": "Module 1: ROS 2",
                        "section": "Introduction",
                        "url": "/module-01-ros2/chapter-01-ros2-architecture",
                        "relevance_score": 0.95
                    }
                ],
                "session_id": "session_123"
            }
        }
