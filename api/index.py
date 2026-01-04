"""
Vercel Serverless API for chatbot
"""
import os
import sys
from pathlib import Path

# Add backend to Python path
backend_path = str(Path(__file__).parent.parent / "backend")
sys.path.insert(0, backend_path)

# Import FastAPI app
from main import app

# Vercel handler
def handler(request, context):
    return app(request, context)
