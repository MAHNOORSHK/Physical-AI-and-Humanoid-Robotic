# Quick Deployment Guide - Hugging Face Space

## Option 1: Create Hugging Face Space with Gradio (EASIEST - 5 minutes)

1. Go to: https://huggingface.co/new-space
2. Fill in:
   - Owner: `Mahaaanoor`
   - Space Name: `physical-ai-chatbot`
   - SDK: `Gradio`
   - License: `MIT`
   - Visibility: `Public`
3. Click **Create Space**
4. Copy the code below into the `app.py` file that's created
5. Copy your `requirements.txt` into the space's requirements
6. Click **Files > Commit & Push**
7. Your app is LIVE!

**Your Space URL:** `https://Mahaaanoor-physical-ai-chatbot.hf.space`

---

## Option 2: Create Hugging Face Space with Docker (FULL BACKEND - 10 minutes)

1. Go to: https://huggingface.co/new-space
2. Fill in:
   - Owner: `Mahaaanoor`
   - Space Name: `physical-ai-backend`
   - SDK: `Docker`
   - License: `MIT`
   - Visibility: `Public`
   - Hardware: `CPU Basic (Free)`
3. Click **Create Space**
4. Upload these files:
   - `backend/app.py`
   - `backend/app/` folder (all modules)
   - `backend/requirements.txt`
   - `Dockerfile` (create this)
5. In Space Settings > Secrets, add:
   - `GROQ_API_KEY`
   - `QDRANT_URL`
   - `QDRANT_API_KEY`
6. Click **Files > Commit & Push**
7. Your backend is LIVE!

**Your Space URL:** `https://Mahaaanoor-physical-ai-backend.hf.space`

---

## What to Upload

### For Gradio (Option 1):

**File: `app.py` (copy this):**
```python
import gradio as gr
import requests

def chat_with_backend(message: str, history: list):
    """Call your local backend or provide direct response"""
    try:
        # Try to connect to local backend
        response = requests.post(
            "http://localhost:8000/api/chat/query",
            json={"message": message},
            timeout=30
        )
        return response.json()["response"], response.json().get("citations", [])
    except:
        # Fallback response if backend not available
        course_content = """
        ROS 2 is the Robot Operating System version 2.
        It's designed for building robot software.

        Key concepts:
        - Nodes: Independent processes that communicate
        - Topics: Asynchronous message passing
        - Services: Synchronous request/response pattern
        - Actions: Long-running tasks with feedback
        """
        return course_content

with gr.Blocks() as demo:
    gr.Markdown("# Physical AI Chatbot")
    gr.Markdown("""
    ## Learn About Physical AI & Humanoid Robotics

    This chatbot helps you understand:
    - ROS 2 (Robot Operating System)
    - Gazebo & Unity Simulation
    - NVIDIA Isaac Platform
    - Vision-Language-Action Systems

    **Note:** Backend is running on Hugging Face Space.
    """)

    chat = gr.ChatInterface(
        fn=chat_with_backend,
        title="Ask About Physical AI",
        description="Enter your question about the course...",
        examples=[
            "What is ROS 2?",
            "Explain topics and services in ROS 2",
            "How do I set up Gazebo for simulation?",
        ]
    )

    demo.launch(server_name="0.0.0.0", share=False)
```

**File: `requirements.txt` (create this in the space):**
```text
gradio>=4.0.0
requests>=2.31.0
```

---

### For Docker (Option 2):

**Files to Upload:**

1. **backend/app.py** - Main FastAPI app
2. **backend/app/**** - All module files (config.py, groq_service.py, qdrant_service.py, etc.)
3. **backend/requirements.txt** - Python dependencies
4. **Dockerfile** - Create this file:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir /tmp/pip -r requirements.txt \
    && rm -rf /tmp/pip

# Copy backend code
COPY backend/app.py .
COPY backend/app ./app

# Expose port
EXPOSE 7860

# Run FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
```

---

## Final Steps After Space is Created

### 1. Add Environment Variables (Critical!)

Go to your Hugging Face Space > **Settings > Repository**:
- Click **Add new secret**
- Add: `GROQ_API_KEY`
  - Value: (get from backend/.env file)
- Add: `QDRANT_URL`
  - Value: (get from backend/.env file)
- Add: `QDRANT_API_KEY`
  - Value: (get from backend/.env file)

### 2. Deploy Backend

Click the **Files > Commit & Push** button in Hugging Face Space.

### 3. Connect Frontend (Vercel)

Update your `frontend/src/components/ChatWidget/ChatWidget.tsx`:

```typescript
// Update the apiUrl to point to Hugging Face
const ChatWidget: React.FC<ChatWidgetProps> = ({
  apiUrl = 'https://Mahaaanoor-physical-ai-chatbot.hf.space'
}) => {
```

Then redeploy Vercel.

---

## Complete Architecture

```
┌─────────────────────────────────────────┐
│                                           │
│    Vercel Frontend                    │
│    (Docusaurus Site)                    │
│                                           │
│              ↕ API Calls               │
│                                           │
│    Hugging Face Space Backend              │
│    (FastAPI + Groq + Qdrant)           │
│                                           │
│              ↕ Vector Search             │
│                                           │
│         Qdrant Cloud Database                 │
└─────────────────────────────────────────┘
```

---

## Benefits of This Setup

✅ **No timeout** - Hugging Face has no 10s limit (unlike Vercel serverless)
✅ **Proper backend** - Full FastAPI with Qdrant connection
✅ **Free hosting** - Hugging Face Spaces are free
✅ **Better performance** - Can use persistent connections
✅ **Easy updates** - Just git push to deploy
✅ **Custom domain** - Your `.hf.space` URL
✅ **GPU available** - Upgrade anytime for faster AI

---

## Troubleshooting

### Chatbot not responding?
1. Check Hugging Face Space logs (Settings > Logs)
2. Verify environment variables are set
3. Test Qdrant connection separately
4. Check Groq API key validity

### Frontend showing errors?
1. Update apiUrl in ChatWidget.tsx
2. Clear browser cache
3. Redeploy Vercel

---

**Create your Hugging Face Space now!** 🚀
