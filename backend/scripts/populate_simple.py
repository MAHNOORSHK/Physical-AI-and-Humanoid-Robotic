"""
Simple script to populate Qdrant with basic embeddings
Uses TF-IDF instead of sentence-transformers to avoid torch dependency
"""
import os
import sys
import asyncio
import hashlib
from pathlib import Path
from typing import List

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.config import settings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


def simple_embedding(text: str, dim: int = 384) -> List[float]:
    """
    Create a simple deterministic embedding from text using hash
    Not as good as transformers but works without PyTorch
    """
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


def parse_markdown_file(file_path: str) -> dict:
    """Parse markdown file and extract metadata"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title from first heading
    lines = content.split('\n')
    title = "Untitled"
    for line in lines:
        if line.startswith('#'):
            title = line.strip('#').strip()
            break

    # Get relative path for URL
    rel_path = file_path.replace('\\', '/').split('docs/')[1] if 'docs/' in file_path else ""
    url = f"/{rel_path.replace('.md', '')}"

    return {
        "title": title,
        "content": content,
        "file_path": file_path,
        "url": url
    }


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    """Split text into overlapping chunks"""
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if len(chunk) > 50:  # Only keep meaningful chunks
            chunks.append(chunk)

    return chunks


async def populate_qdrant():
    """Main function to populate Qdrant"""
    print("Starting Qdrant population...")

    # Initialize Qdrant client
    client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY
    )

    # Create collection
    print("Creating Qdrant collection...")
    try:
        collections = client.get_collections().collections
        collection_names = [col.name for col in collections]

        if settings.QDRANT_COLLECTION_NAME in collection_names:
            print("Deleting existing collection...")
            client.delete_collection(settings.QDRANT_COLLECTION_NAME)

        client.create_collection(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(
                size=settings.QDRANT_VECTOR_SIZE,
                distance=Distance.COSINE
            )
        )
        print(f"Created collection: {settings.QDRANT_COLLECTION_NAME}")
    except Exception as e:
        print(f"Error creating collection: {e}")
        return

    # Find all markdown files
    docs_dir = Path(__file__).parent.parent.parent / "frontend" / "docs"
    md_files = list(docs_dir.rglob("*.md"))

    print(f"Found {len(md_files)} markdown files\n")

    # Process each file
    total_chunks = 0
    points = []

    for idx, md_file in enumerate(md_files):
        print(f"Processing ({idx+1}/{len(md_files)}): {md_file.name}")

        # Parse file
        doc = parse_markdown_file(str(md_file))

        # Determine chapter and section from path
        chapter = "General"
        section = doc['title']

        if 'module-01-ros2' in str(md_file):
            chapter = "Module 1: ROS 2"
        elif 'module-02-simulation' in str(md_file):
            chapter = "Module 2: Simulation"
        elif 'module-03-isaac' in str(md_file):
            chapter = "Module 3: NVIDIA Isaac"
        elif 'module-04-vla' in str(md_file):
            chapter = "Module 4: VLA Systems"

        # Chunk the content
        chunks = chunk_text(doc['content'], chunk_size=500, overlap=50)
        print(f"  Split into {len(chunks)} chunks")

        # Generate embeddings for each chunk
        for chunk_idx, chunk in enumerate(chunks):
            # Generate embedding
            embedding = simple_embedding(chunk, dim=settings.QDRANT_VECTOR_SIZE)

            # Prepare metadata - use simple integer ID
            vector_id = total_chunks + 1
            metadata = {
                "chapter": chapter,
                "section": section,
                "url": doc['url'],
                "content": chunk,
                "file": md_file.name
            }

            point = PointStruct(
                id=vector_id,
                vector=embedding,
                payload=metadata
            )
            points.append(point)

            total_chunks += 1

            # Batch upload every 50 chunks
            if len(points) >= 50:
                print(f"  Uploading batch of {len(points)} vectors...")
                client.upsert(
                    collection_name=settings.QDRANT_COLLECTION_NAME,
                    points=points
                )
                points = []

    # Upload remaining chunks
    if points:
        print(f"\nUploading final batch of {len(points)} vectors...")
        client.upsert(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            points=points
        )

    print(f"\n[SUCCESS] Populated Qdrant!")
    print(f"Total chunks: {total_chunks}")
    print(f"Total files: {len(md_files)}")

    # Get collection info
    info = client.get_collection(settings.QDRANT_COLLECTION_NAME)
    print(f"\nQdrant Collection Info:")
    print(f"  Name: {settings.QDRANT_COLLECTION_NAME}")
    print(f"  Vectors: {info.points_count}")
    print(f"  Dimension: {info.config.params.vectors.size}")


if __name__ == "__main__":
    asyncio.run(populate_qdrant())
