# RAG Chatbot Setup Guide

This guide will help you test and integrate the RAG chatbot with your Physical AI textbook.

## 🧪 Step 1: Test with Mock Responses (Current Setup)

The chatbot is ready to test RIGHT NOW without any API keys!

### Start the Backend (Test Mode)

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Backend will start at: http://localhost:8000

You should see: `🧪 Running in TEST MODE (mock responses)`

### Start the Frontend

```bash
cd frontend
npm start
```

Frontend will start at: http://localhost:3000/hackathon-I/

### Test the Chatbot

1. Open http://localhost:3000/hackathon-I/ in your browser
2. You'll see a purple chat button (💬) in the bottom-right corner
3. Click it to open the chat widget
4. Try these example queries:
   - "What is ROS 2?"
   - "How do topics work?"
   - "Tell me about Gazebo simulation"
   - "What is NVIDIA Isaac?"

5. **Select text feature**:
   - Highlight any text from the course content
   - Click "Ask AI about selection" button
   - The chatbot will explain the selected text

### Test Mode Features

- Intelligent keyword-based responses
- Mock citations with chapter references
- Session management
- Text selection context
- No API costs!

---

## 🚀 Step 2: Production Mode with Real APIs

Once you're ready, follow these steps to enable full functionality:

### 2.1 Create OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-...`)
5. **Cost**: Pay-as-you-go (~$0.002 per query)

### 2.2 Create Qdrant Cloud Database

1. Go to https://cloud.qdrant.io/
2. Sign up for free account
3. Click "Create Cluster"
4. Choose "Free Tier" (1GB storage, 100K vectors)
5. Copy:
   - Cluster URL (e.g., `https://xxx.qdrant.io`)
   - API Key

### 2.3 Create Neon Postgres Database (Optional)

For conversation history:

1. Go to https://neon.tech/
2. Sign up for free account
3. Create a new project
4. Copy the connection string (starts with `postgres://...`)

### 2.4 Update Environment Variables

Edit `backend/.env`:

```env
# Switch to production mode
TEST_MODE=false

# OpenAI Configuration
OPENAI_API_KEY=sk-your-actual-key-here

# Qdrant Configuration
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-key-here

# Neon Postgres (optional for history)
DATABASE_URL=postgres://your-connection-string

# Keep existing settings
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### 2.5 Populate Qdrant with Course Content

You'll need to create embeddings for the course content. I can help you create a script for this:

```python
# backend/scripts/populate_embeddings.py
# This will:
# 1. Parse all markdown files from frontend/docs/
# 2. Generate embeddings for each section
# 3. Upload to Qdrant with metadata (chapter, section, url)
```

**Would you like me to create this script now?**

### 2.6 Restart Backend in Production Mode

```bash
cd backend
python main.py
```

You should see: `🚀 Running in PRODUCTION MODE (real APIs)`

---

## 📊 API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Chat Query
```bash
curl -X POST http://localhost:8000/api/chat/query \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is ROS 2?",
    "session_id": "test-session"
  }'
```

### Collection Info
```bash
curl http://localhost:8000/api/collection/info
```

---

## 🎨 ChatWidget Features

### Already Implemented:
✅ Floating chat button with gradient design
✅ Collapsible chat panel
✅ Message history with user/assistant bubbles
✅ Text selection context feature
✅ Citation references with relevance scores
✅ Quick action buttons
✅ Loading states with typing indicator
✅ Dark mode support
✅ Responsive design (mobile-friendly)
✅ Session management
✅ Clear chat functionality

### Chat Widget Props:

```tsx
<ChatWidget
  apiUrl="http://localhost:8000"  // Backend URL
/>
```

---

## 🔧 Troubleshooting

### Backend won't start
- Check Python version: `python --version` (need 3.8+)
- Install dependencies: `pip install -r requirements.txt`
- Check port 8000 is free: `netstat -ano | findstr :8000`

### Frontend won't connect to backend
- Check CORS settings in `backend/main.py`
- Verify backend is running at http://localhost:8000
- Check browser console for errors (F12)

### Chatbot button not appearing
- Clear browser cache
- Check browser console for React errors
- Verify `frontend/src/theme/Root.tsx` exists

### Mock responses not working
- Verify `TEST_MODE=true` in `.env`
- Check backend logs for errors

---

## 📝 Next Steps

1. **Test the UI**: Open frontend and interact with chatbot
2. **Get API Keys**: Follow Step 2 above when ready
3. **Generate Embeddings**: I can create a script to populate Qdrant
4. **Write More Content**: Complete Module 2-4 chapters
5. **Deploy**: Host on Vercel (frontend) + Railway (backend)

---

## 💡 Tips

- Start with test mode to develop UI and features
- Generate embeddings incrementally as you write content
- Monitor OpenAI usage at https://platform.openai.com/usage
- Use free tiers: Qdrant (1GB), Neon (512MB)
- Citations link back to course sections automatically

---

## 🤔 Questions?

Ask me anything! For example:
- "Create the embedding population script"
- "How do I deploy this to production?"
- "Add a feature to [describe feature]"
- "Fix error: [paste error message]"

Let's make this chatbot amazing! 🚀
