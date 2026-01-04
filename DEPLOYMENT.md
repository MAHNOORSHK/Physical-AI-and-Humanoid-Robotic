# Deployment Guide - Vercel

## Prerequisites
- Vercel account
- GitHub repository connected to Vercel
- API Keys ready (Groq, Qdrant)

## Step 1: Connect GitHub to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click "Import Project"
3. Select your GitHub repository: `MAHNOORSHK/Physical-AI-and-Humanoid-Robotic`
4. Click "Import"

## Step 2: Configure Environment Variables

In Vercel dashboard, go to **Settings > Environment Variables** and add:

### Required Variables:
```
GROQ_API_KEY=your_groq_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

**Note:** Get the actual API keys from your `.env` file in the backend folder.

Make sure to add these for **Production**, **Preview**, and **Development** environments.

## Step 3: Configure Build Settings

In Vercel project settings:

- **Framework Preset**: Other
- **Build Command**: `cd frontend && npm install && npm run build`
- **Output Directory**: `frontend/build`
- **Install Command**: `cd frontend && npm install`

## Step 4: Deploy

1. Click "Deploy"
2. Wait for build to complete
3. Your site will be live at: `https://physical-ai-and-humanoid-robotic.vercel.app`

## Step 5: Test Chatbot

1. Visit your deployed site
2. Click the chatbot icon (bottom-right)
3. Ask a question like "What is ROS 2?"
4. Verify the response is coming from the backend

## Troubleshooting

### Backend API Not Working
- Check environment variables are set correctly
- Verify Qdrant has data (should have 22 vectors)
- Check Vercel function logs for errors

### Frontend Not Loading
- Verify build completed successfully
- Check Output Directory is set to `frontend/build`
- Look for build errors in deployment logs

### CORS Errors
- Backend is configured to allow all origins in production
- If issues persist, check `backend/main.py` CORS settings

## Update Deployment

To update the site after making changes:
```bash
git add .
git commit -m "Your update message"
git push origin master
```

Vercel will automatically rebuild and deploy.

## Custom Domain (Optional)

1. Go to Vercel project settings
2. Click "Domains"
3. Add your custom domain
4. Update DNS records as instructed
