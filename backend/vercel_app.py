"""
Vercel-compatible FastAPI app
"""
from main import app

# Export for Vercel
handler = app
