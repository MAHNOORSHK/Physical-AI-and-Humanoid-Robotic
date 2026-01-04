"""
Vercel Serverless API endpoint for chatbot
"""
import sys
from pathlib import Path

# Add backend to path
backend_path = str(Path(__file__).parent.parent / "backend")
sys.path.insert(0, backend_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.main import app

# Export the FastAPI app for Vercel
handler = app
