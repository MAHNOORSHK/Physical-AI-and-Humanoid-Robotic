"""
OpenAI service for chat completions and embeddings
"""

from typing import List, Dict
from openai import OpenAI
from app.config import settings


class OpenAIService:
    """Service for interacting with OpenAI API"""

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.embedding_model = settings.OPENAI_EMBEDDING_MODEL

    async def generate_chat_response(
        self,
        user_message: str,
        context_documents: List[Dict[str, str]],
        conversation_history: List[Dict[str, str]] = None
    ) -> str:
        """
        Generate chat response using RAG

        Args:
            user_message: User's question
            context_documents: Retrieved documents from Qdrant
            conversation_history: Previous messages

        Returns:
            AI-generated response
        """
        # Build context from retrieved documents
        context_text = "\n\n".join([
            f"[{doc.get('chapter', 'Unknown')} - {doc.get('section', 'Unknown')}]\n{doc.get('content', '')}"
            for doc in context_documents
        ])

        # System prompt optimized for educational context
        system_prompt = f"""You are an expert teaching assistant for a Physical AI and Humanoid Robotics course.

Your role is to help students learn about:
- ROS 2 (Robot Operating System)
- Gazebo and Unity simulation
- NVIDIA Isaac platform
- Vision-Language-Action systems
- Humanoid robotics

INSTRUCTIONS:
1. Answer questions accurately using the provided course context
2. If the context doesn't contain relevant information, say so honestly
3. Provide clear, educational explanations suitable for students
4. Reference specific chapters/sections when relevant
5. Be concise but comprehensive
6. Use examples and analogies when helpful

COURSE CONTEXT:
{context_text}

Remember: You're helping students learn robotics and Physical AI. Be encouraging and supportive!
"""

        # Build messages
        messages = [{"role": "system", "content": system_prompt}]

        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)

        # Add current user message
        messages.append({"role": "user", "content": user_message})

        # Generate response
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=settings.OPENAI_MAX_TOKENS,
            temperature=settings.OPENAI_TEMPERATURE
        )

        return response.choices[0].message.content

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for text

        Args:
            text: Input text to embed

        Returns:
            Embedding vector (list of floats)
        """
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=text
        )

        return response.data[0].embedding

    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=texts
        )

        return [item.embedding for item in response.data]
