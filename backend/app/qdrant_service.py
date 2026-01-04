"""
Qdrant vector database service for semantic search
"""

from typing import List, Dict, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter
from app.config import settings


class QdrantService:
    """Service for interacting with Qdrant vector database"""

    def __init__(self):
        """Initialize Qdrant client"""
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY
        )
        self.collection_name = settings.QDRANT_COLLECTION_NAME
        self.vector_size = settings.QDRANT_VECTOR_SIZE

    async def create_collection(self):
        """Create Qdrant collection if it doesn't exist"""
        try:
            collections = self.client.get_collections().collections
            collection_names = [col.name for col in collections]

            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.vector_size,
                        distance=Distance.COSINE
                    )
                )
                print(f"✓ Created collection: {self.collection_name}")
            else:
                print(f"✓ Collection already exists: {self.collection_name}")

        except Exception as e:
            print(f"Error creating collection: {e}")
            raise

    async def insert_embedding(
        self,
        vector_id: str,
        embedding: List[float],
        metadata: Dict[str, str]
    ) -> bool:
        """
        Insert single embedding into Qdrant

        Args:
            vector_id: Unique identifier
            embedding: Embedding vector
            metadata: Chapter, section, url, content

        Returns:
            Success status
        """
        try:
            point = PointStruct(
                id=vector_id,
                vector=embedding,
                payload=metadata
            )

            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )

            return True

        except Exception as e:
            print(f"Error inserting embedding: {e}")
            return False

    async def insert_embeddings_batch(
        self,
        vector_ids: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict[str, str]]
    ) -> bool:
        """
        Insert multiple embeddings in batch

        Args:
            vector_ids: List of unique identifiers
            embeddings: List of embedding vectors
            metadatas: List of metadata dicts

        Returns:
            Success status
        """
        try:
            points = [
                PointStruct(id=vid, vector=emb, payload=meta)
                for vid, emb, meta in zip(vector_ids, embeddings, metadatas)
            ]

            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            print(f"✓ Inserted {len(points)} embeddings")
            return True

        except Exception as e:
            print(f"Error inserting batch: {e}")
            return False

    async def search_similar(
        self,
        query_embedding: List[float],
        top_k: int = None
    ) -> List[Dict]:
        """
        Search for similar documents

        Args:
            query_embedding: Query vector
            top_k: Number of results (default from settings)

        Returns:
            List of similar documents with metadata and scores
        """
        if top_k is None:
            top_k = settings.TOP_K_RESULTS

        try:
            search_result = self.client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                limit=top_k
            ).points

            results = []
            for scored_point in search_result:
                result = {
                    "id": scored_point.id,
                    "score": scored_point.score,
                    "chapter": scored_point.payload.get("chapter", "Unknown"),
                    "section": scored_point.payload.get("section", "Unknown"),
                    "url": scored_point.payload.get("url", "/"),
                    "content": scored_point.payload.get("content", "")
                }
                results.append(result)

            return results

        except Exception as e:
            print(f"Error searching: {e}")
            return []

    async def get_collection_info(self) -> Dict:
        """Get collection statistics"""
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "name": info.name,
                "vector_count": info.points_count,
                "vector_size": info.config.params.vectors.size
            }
        except Exception as e:
            print(f"Error getting info: {e}")
            return {}
