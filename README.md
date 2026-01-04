# Physical AI & Humanoid Robotics Textbook

Interactive textbook with RAG-powered chatbot for learning Physical AI and Humanoid Robotics.

## Project Structure

```
hackathon-I/
├── .specify/           # Project specifications and memory
├── frontend/           # Docusaurus textbook website
├── backend/            # FastAPI RAG chatbot backend
├── specs/              # Technical specifications
└── README.md
```

## Quick Start

### Frontend (Book)
```bash
cd frontend
npm install
npm start
```

### Backend (Chatbot)
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

## Features

- 📚 Interactive textbook on Physical AI & Robotics
- 🤖 RAG-powered chatbot with context-aware responses
- 🔍 Text selection for contextual queries
- 📖 Source citations linking back to book sections

## Tech Stack

**Frontend:** Docusaurus, React, TypeScript
**Backend:** FastAPI, OpenAI, Qdrant, Neon Postgres

## Development Status

- [x] Project setup
- [ ] Frontend book content
- [ ] Backend API implementation
- [ ] RAG integration
- [ ] Deployment
