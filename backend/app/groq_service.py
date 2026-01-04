"""
Groq AI service for chat completions
Uses Llama models via Groq API
"""

from typing import List, Dict
from groq import Groq
from app.config import settings


class GroqService:
    """Service for interacting with Groq AI"""

    def __init__(self):
        """Initialize Groq client"""
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL

    async def generate_chat_response(
        self,
        user_message: str,
        context_documents: List[Dict[str, str]],
        conversation_history: List[Dict[str, str]] = None
    ) -> str:
        """
        Generate chat response using Groq with RAG context

        Args:
            user_message: User's question
            context_documents: Retrieved documents from Qdrant
            conversation_history: Previous conversation (optional)

        Returns:
            AI-generated response
        """
        # Build context from retrieved documents
        context_text = "\n\n".join([
            f"[Source: {doc['chapter']} - {doc['section']}]\n{doc['content']}"
            for doc in context_documents[:3]  # Top 3 most relevant
        ])

        # System prompt for educational assistant
        system_prompt = """You are an expert AI assistant for a Physical AI and Humanoid Robotics course.
Your role is to help students learn about:
- ROS 2 (Robot Operating System)
- Gazebo and Unity simulation
- NVIDIA Isaac platform
- Vision-Language-Action systems

Guidelines:
1. Answer based on the provided context from the course
2. Be clear, concise, and educational
3. Use technical terms but explain them simply
4. If the question is outside the course scope, politely redirect to course topics
5. Keep responses 3-5 sentences unless more detail is needed
6. Use examples when helpful"""

        # Build messages
        messages = [
            {"role": "system", "content": system_prompt}
        ]

        # Add conversation history if available
        if conversation_history:
            messages.extend(conversation_history[-4:])  # Last 2 exchanges

        # Add context and user query
        user_prompt = f"""Context from the course:
{context_text}

Student Question: {user_message}

Please answer the student's question based on the context provided. If the context doesn't contain relevant information, provide a general answer related to the course topics and suggest they refer to specific course modules."""

        messages.append({"role": "user", "content": user_prompt})

        try:
            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
                top_p=0.9
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"Groq API error: {e}")
            return f"I encountered an error processing your question. Please try again or rephrase your question."

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using simple hash-based approach
        Note: Groq doesn't provide embeddings, so we use deterministic hash
        """
        import hashlib

        dim = 384  # Must match Qdrant vector size

        # Create multiple hashes for better distribution
        embeddings = []
        for i in range(dim // 32):
            hash_input = f"{text}_{i}"
            hash_obj = hashlib.sha256(hash_input.encode())
            hash_bytes = hash_obj.digest()

            for j in range(0, len(hash_bytes), 4):
                if len(embeddings) >= dim:
                    break
                # Convert 4 bytes to float
                val = int.from_bytes(hash_bytes[j:j+4], 'big')
                # Normalize to [-1, 1]
                normalized = (val / (2**32)) * 2 - 1
                embeddings.append(normalized)

        # Ensure exact dimension
        while len(embeddings) < dim:
            embeddings.append(0.0)

        return embeddings[:dim]
