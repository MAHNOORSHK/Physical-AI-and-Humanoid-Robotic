"""
Script to populate Qdrant with book embeddings
Reads markdown files, generates embeddings, and uploads to Qdrant
"""

import os
import sys
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.config import settings
from app.qdrant_service import QdrantService
from sentence_transformers import SentenceTransformer

# Use sentence-transformers for embeddings (free and works offline)
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # 384 dimensions


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
    print("🚀 Starting Qdrant population...")

    # Initialize Qdrant service
    qdrant = QdrantService()

    # Create collection
    print("📦 Creating Qdrant collection...")
    await qdrant.create_collection()

    # Find all markdown files
    docs_dir = Path(__file__).parent.parent.parent / "frontend" / "docs"
    md_files = list(docs_dir.rglob("*.md"))

    print(f"📚 Found {len(md_files)} markdown files")

    # Process each file
    total_chunks = 0
    vector_ids = []
    embeddings = []
    metadatas = []

    for idx, md_file in enumerate(md_files):
        print(f"\n📄 Processing ({idx+1}/{len(md_files)}): {md_file.name}")

        # Parse file
        doc = parse_markdown_file(str(md_file))

        # Determine chapter and section from path
        path_parts = str(md_file).split(os.sep)
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
        print(f"   Split into {len(chunks)} chunks")

        # Generate embeddings for each chunk
        for chunk_idx, chunk in enumerate(chunks):
            # Generate embedding
            embedding = embedding_model.encode(chunk).tolist()

            # Prepare metadata
            vector_id = f"{md_file.stem}_chunk_{chunk_idx}"
            metadata = {
                "chapter": chapter,
                "section": section,
                "url": doc['url'],
                "content": chunk,
                "file": md_file.name
            }

            vector_ids.append(vector_id)
            embeddings.append(embedding)
            metadatas.append(metadata)

            total_chunks += 1

            # Batch upload every 50 chunks
            if len(vector_ids) >= 50:
                print(f"   ⬆️  Uploading batch of {len(vector_ids)} vectors...")
                await qdrant.insert_embeddings_batch(vector_ids, embeddings, metadatas)
                vector_ids = []
                embeddings = []
                metadatas = []

    # Upload remaining chunks
    if vector_ids:
        print(f"\n⬆️  Uploading final batch of {len(vector_ids)} vectors...")
        await qdrant.insert_embeddings_batch(vector_ids, embeddings, metadatas)

    print(f"\n✅ Successfully populated Qdrant!")
    print(f"📊 Total chunks: {total_chunks}")
    print(f"📚 Total files: {len(md_files)}")

    # Get collection info
    info = await qdrant.get_collection_info()
    print(f"\n📈 Qdrant Collection Info:")
    print(f"   Name: {info.get('name')}")
    print(f"   Vectors: {info.get('vector_count')}")
    print(f"   Dimension: {info.get('vector_size')}")


if __name__ == "__main__":
    asyncio.run(populate_qdrant())
