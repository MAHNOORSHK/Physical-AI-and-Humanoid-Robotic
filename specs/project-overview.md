# Project Overview

**Project:** Physical AI & Humanoid Robotics Interactive Textbook

## Components

### 1. Frontend (Docusaurus)
- Interactive book with 4 modules
- 10-15 chapters on ROS 2, Simulation, NVIDIA Isaac, VLA
- Embedded chatbot widget

### 2. Backend (FastAPI)
- RAG-powered chatbot
- OpenAI integration
- Qdrant vector database
- Neon Postgres for conversation history

### 3. Integration
- Chat widget embedded in all pages
- Text selection for context queries
- Citations with links to book sections

## Tech Stack

- **Frontend:** Docusaurus, React, TypeScript
- **Backend:** FastAPI, Python
- **AI:** OpenAI GPT-4 + Embeddings
- **Databases:** Qdrant (vector), Neon Postgres (relational)
- **Deployment:** GitHub Pages (frontend), Vercel/Railway (backend)
