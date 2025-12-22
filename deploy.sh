#!/bin/bash
# Deploy Elicitron to Google Cloud Run

# Set variables
PROJECT_ID="your-gcp-project-id"
REGION="us-central1"
SERVICE_NAME="elicitron-backend"
API_KEY="your_gemini_api_key_here"

echo "🚀 Deploying Elicitron Backend to Google Cloud Run..."

# Build and deploy backend
gcloud run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=$API_KEY \
  --memory 512Mi \
  --timeout 300

echo "✅ Backend deployed!"
echo "📝 Copy the backend URL and update react-frontend/src/App.js"
echo ""
echo "Next steps:"
echo "1. Update REACT_APP_API_URL in react-frontend"
echo "2. Build frontend: cd react-frontend && npm run build"
echo "3. Deploy to Cloud Storage or Vercel"
