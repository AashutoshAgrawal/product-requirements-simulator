# 🎯 Elicitron - AI-Powered Requirements Elicitation

A production-grade **FastAPI + React** application that automates requirements elicitation using the Elicitron methodology with Google's Gemini AI.

## 🚀 Quick Start - Production Deployment

### Prerequisites
✅ Application running locally (both services)
✅ GitHub repository: AashutoshAgrawal/product-requirements-simulator
✅ render.yaml created with auto-scaling config
✅ Health check endpoint: `/api/health`

### Deploy to Production (5 minutes)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add deployment configs"
   git push origin main
   ```

2. **Deploy to Render** (Backend + Frontend)
   - Go to https://render.com → Sign up with GitHub
   - Click "New +" → "Blueprint"
   - Select: `AashutoshAgrawal/product-requirements-simulator`
   - Add environment variable: `GOOGLE_API_KEY=AIzaSyC1HBVK2XY-gebCyE6N77q6IsklqMRRfxY`
   - Click "Apply" → Wait 5-10 minutes
   - **Backend URL**: `https://elicitron-backend.onrender.com`
   - **Frontend URL**: `https://elicitron-frontend.onrender.com`

3. **Verify Deployment**
   ```bash
   # Test health check
   curl https://elicitron-backend.onrender.com/api/health
   
   # Open frontend
   open https://elicitron-frontend.onrender.com
   ```

4. **Test Analysis** (1-5 agents, 30-150 seconds)
   - Enter product description
   - Select number of agents
   - Monitor real-time progress
   - Download JSON results

**That's it!** 🎉 Free, scalable, production-ready deployment.

For detailed scaling, monitoring, and troubleshooting: See **Step-by-Step Guide** below.

---

## 🏗️ Architecture

**Modern Production Stack:**
- **Backend:** FastAPI 0.115.0 (async Python web framework, 2-3x faster than Flask)
- **Frontend:** React 18.3.1 (modern component-based UI)
- **AI Model:** Google Gemini 2.5 Flash
- **Server:** Uvicorn (high-performance ASGI server)
- **Deployment:** Render.com (auto-scaling, zero-downtime)

**Key Features:**
- 🔄 Async background processing for long-running analysis tasks (152s+)
- 📊 Real-time progress tracking with stage-by-stage updates
- 📚 Auto-generated API documentation (Swagger UI at `/docs`, ReDoc at `/redoc`)
- 🔒 Type-safe request/response validation with Pydantic models
- 🎨 Modern responsive UI with gradient design
- 📥 JSON export of analysis results
- 🌐 CORS-enabled for seamless frontend-backend communication
- 📈 **Auto-scaling** for future growth (1-5 agents → 50+ agents)

## 🎯 Methodology

This system automates the 4-stage **Elicitron requirements elicitation** process:

1. **Agent Generation** - Create diverse user personas with varied demographics and backgrounds
2. **Experience Simulation** - Simulate realistic user interactions (Action/Observation/Challenge format)
3. **Interview Simulation** - Conduct structured follow-up interviews based on experiences
4. **Latent Need Extraction** - Extract, classify, and prioritize underlying user needs

## 🏗️ Project Structure

```
product-requirements-simulator/
│
├── app_fastapi.py                # 🚀 FastAPI backend (main production API)
├── app.py                        # 🗄️ Legacy Flask app (deprecated, kept for reference)
├── Dockerfile                    # 🐳 Backend Docker image
├── docker-compose.yml            # 🎼 Multi-container orchestration
├── requirements.txt              # 📦 Python dependencies
│
├── react-frontend/               # ⚛️ React Frontend Application
│   ├── public/
│   │   └── index.html           # HTML template
│   ├── src/
│   │   ├── App.js               # Main React component with full UI
│   │   ├── App.css              # Gradient styling and responsive design
│   │   ├── index.js             # React app entry point
│   │   └── index.css            # Global CSS styles
│   ├── Dockerfile               # 🐳 Frontend Docker image (multi-stage with nginx)
│   ├── nginx.conf               # Nginx reverse proxy configuration
│   ├── package.json             # Node.js dependencies (React 18, Axios)
│   └── .dockerignore            # Docker build exclusions
│
├── src/                          # 🔧 Core Elicitron Pipeline
│   ├── llm/                     # LLM Integration Layer
│   │   ├── gemini_client.py     # Multi-tier Gemini API client
│   │   └── prompts/             # Prompt engineering templates
│   │       ├── agent_generation.txt
│   │       ├── experience_simulation.txt
│   │       ├── interview.txt
│   │       └── latent_classifier.txt
│   │
│   ├── agents/                  # Agent Operations
│   │   ├── generator.py         # User persona generation
│   │   ├── simulator.py         # Experience simulation
│   │   ├── interviewer.py       # Interview conduction
│   │   └── latent_extractor.py  # Need extraction & classification
│   │
│   ├── pipeline/                # Orchestration
│   │   └── pipeline.py          # End-to-end 4-stage workflow
│   │
│   └── utils/                   # Utilities
│       ├── logger.py            # Logging configuration
│       └── json_parser.py       # Safe JSON parsing with validation
│
├── config/                      # Configuration Files
│   ├── settings.yaml            # System settings
│   └── interview_questions.yaml # Structured interview questions
│
├── tests/                       # Test Suite
│   ├── test_pipeline.py
│   ├── test_agents.py
│   └── test_latent_extraction.py
│
├── .dockerignore                # Docker build exclusions
├── .env                         # Environment variables (not committed)
└── README.md                    # This file
```

## 📦 Installation & Setup

### Option 1: Docker Deployment (Recommended for Production)

**Prerequisites:**
- Docker 20.10+
- Docker Compose 1.29+
- Google Gemini API key ([Get one free](https://makersuite.google.com/app/apikey))

**Steps:**

1. **Clone the repository**
   ```bash
   git clone https://github.com/AashutoshAgrawal/product-requirements-simulator.git
   cd product-requirements-simulator
   ```

2. **Set environment variables**
   ```bash
   cp .env.example .env
   nano .env  # Add your Google API key
   ```

   Add to `.env`:
   ```
   GOOGLE_API_KEY=your_actual_gemini_api_key_here
   ```

3. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs (Swagger): http://localhost:8000/docs
   - API Docs (ReDoc): http://localhost:8000/redoc

### Option 2: Local Development Setup

**Prerequisites:**
- Python 3.11+
- Node.js 18+
- npm or yarn
- Google Gemini API key

**Backend Setup:**

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**
   ```bash
   cp .env.example .env
   nano .env  # Add your API key
   ```

4. **Run FastAPI backend**
   ```bash
   # Option 1: Direct Python execution
   python app_fastapi.py

   # Option 2: Using uvicorn with auto-reload (recommended for development)
   uvicorn app_fastapi:app --reload --host 0.0.0.0 --port 8000
   ```

   Backend will be available at:
   - API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

**Frontend Setup:**

1. **Navigate to frontend directory**
   ```bash
   cd react-frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```

   Frontend will open automatically at http://localhost:3000

## 🎮 Usage

### Web Interface (React UI)

1. **Navigate to http://localhost:3000**
2. **Fill in the analysis form:**
   - **Product Name:** e.g., "camping tent", "smartphone", "office chair"
   - **Design Context:** e.g., "ultralight backpacking in alpine conditions"
   - **Number of Agents:** 1-5 personas (more = comprehensive analysis)
3. **Click "Start Analysis"**
4. **Monitor real-time progress** through 5 stages:
   - Initializing
   - Generating Agents
   - Simulating Experiences
   - Conducting Interviews
   - Extracting Needs
5. **View results:**
   - Agent personas with demographics
   - Categorized needs (Functional, Emotional, Social)
   - Priority levels (High/Medium/Low)
   - Evidence and design implications
6. **Download results** as JSON for further processing

### API Usage (cURL / Postman)

**Start Analysis:**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "product": "camping tent",
    "design_context": "ultralight backpacking in alpine conditions",
    "n_agents": 3
  }'
```

Response:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "message": "Analysis job started"
}
```

**Check Status:**
```bash
curl http://localhost:8000/api/status/550e8400-e29b-41d4-a716-446655440000
```

Response:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "progress": {
    "stage": "conducting_interviews",
    "message": "Running interviews for 3 agents..."
  }
}
```

**Get Results:**
```bash
curl http://localhost:8000/api/results/550e8400-e29b-41d4-a716-446655440000
```

### API Endpoints Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check and API info |
| POST | `/api/analyze` | Start new analysis job |
| GET | `/api/status/{job_id}` | Check job status and progress |
| GET | `/api/results/{job_id}` | Get completed results |
| GET | `/api/jobs` | List all jobs (admin) |
| DELETE | `/api/jobs/{job_id}` | Delete a job |
| GET | `/docs` | Swagger UI (interactive API docs) |
| GET | `/redoc` | ReDoc (alternative API docs) |

## 🚢 Deployment Options

### Google Cloud Run (Recommended)

**Pros:** Fully managed, auto-scaling, pay-per-use, free tier available

1. **Install Google Cloud SDK**
   ```bash
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL
   gcloud init
   ```

2. **Build and push backend**
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/elicitron-backend
   gcloud run deploy elicitron-backend \
     --image gcr.io/YOUR_PROJECT_ID/elicitron-backend \
     --platform managed \
     --region us-central1 \
     --set-env-vars GOOGLE_API_KEY=your_key
   ```

3. **Build and push frontend**
   ```bash
   cd react-frontend
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/elicitron-frontend
   gcloud run deploy elicitron-frontend \
     --image gcr.io/YOUR_PROJECT_ID/elicitron-frontend \
     --platform managed \
     --region us-central1
   ```

### Render.com (Easiest Free Option)

**Pros:** Simple deployment, free tier, automatic SSL

1. **Create account at render.com**
2. **Create Web Service for backend:**
   - Connect GitHub repository
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app_fastapi:app --host 0.0.0.0 --port $PORT`
   - Environment: Add `GOOGLE_API_KEY`
3. **Create Static Site for frontend:**
   - Root Directory: `react-frontend`
   - Build Command: `npm install && npm run build`
   - Publish Directory: `build`

### Railway.app

**Pros:** Simple, Git-based deployments, free tier

1. **Create account at railway.app**
2. **New Project → Deploy from GitHub**
3. **Add environment variables**
4. **Railway auto-detects Dockerfile and deploys**

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_pipeline.py

# Run with coverage
pytest --cov=src tests/

# Verbose output
pytest -v
```

## 📊 Example Output

**Input:**
- Product: "camping tent"
- Context: "ultralight backpacking in alpine conditions"
- Agents: 3

**Output Structure:**
```json
{
  "agents": ["Agent 1 persona...", "Agent 2 persona...", "Agent 3 persona..."],
  "aggregated_needs": {
    "total_needs": 12,
    "categories": {
      "Functional": [
        {
          "need_statement": "Tent must withstand winds up to 60mph",
          "priority": "High",
          "evidence": "Agent experienced tent collapse in storm...",
          "design_implication": "Reinforce pole structure and guy lines"
        }
      ],
      "Emotional": [...],
      "Social": [...]
    }
  },
  "metadata": {
    "product": "camping tent",
    "design_context": "ultralight backpacking...",
    "n_agents": 3
  }
}
```

## 🔧 Configuration

**System Settings** (`config/settings.yaml`):
- LLM temperature and model parameters
- Retry logic and timeouts
- Logging levels

**Interview Questions** (`config/interview_questions.yaml`):
- Follow-up question templates
- Context-specific probes

---

## 📈 Scalability & Production Guide

### Current Configuration (Free Tier)
✅ **Auto-Scaling**: Enabled on Render starter plan
✅ **Health Monitoring**: `/api/health` endpoint (pinged every 30s)
✅ **Zero-Downtime Deploys**: Rolling updates on git push
✅ **Long-Running Tasks**: Backend handles 152s+ analysis (no timeout)

### Performance Metrics
- **1 agent**: ~30 seconds
- **3 agents**: ~90 seconds
- **5 agents**: ~150 seconds
- **Cold start**: ~30 seconds (free tier sleeps after 15 min inactivity)

### Scaling Strategy

#### Phase 1: Current (1-10 agents)
- **Plan**: Free tier (Render starter)
- **Cost**: $0/month
- **Capacity**: 
  - 750 service hours/month
  - 100+ concurrent requests
  - 512MB RAM per instance
- **Limitation**: Cold starts after 15 min inactivity

#### Phase 2: Growth (10-50 agents)
- **Plan**: Render Standard ($25/month)
- **Upgrades**:
  - Always-on (no cold starts)
  - 2GB RAM per instance
  - Faster CPU (2x performance)
  - Horizontal auto-scaling
- **Add Redis Queue**:
  ```yaml
  # In render.yaml, add:
  - type: redis
    name: elicitron-queue
    plan: free
    maxmemoryPolicy: allkeys-lru
  ```
  
  Update `app_fastapi.py`:
  ```python
  # Use Celery + Redis for background jobs
  # Handles 50+ concurrent analyses
  ```

#### Phase 3: Scale (50+ agents)
- **Plan**: Render Pro ($85/month)
- **Features**:
  - Multiple auto-scaling instances
  - 4GB RAM per instance
  - Priority support
- **Add PostgreSQL**:
  ```yaml
  # In render.yaml, add:
  - type: postgres
    name: elicitron-db
    plan: free  # 1GB storage
    databaseName: elicitron
    databaseUser: elicitron
  ```
  
  For persistent job history and user data.

### Monitoring & Alerts

**Render Dashboard Metrics**:
1. **Performance**: CPU, RAM, response time
2. **Logs**: Real-time application logs
3. **Deploys**: Deployment history with rollback
4. **Events**: Auto-scaling, restarts, errors

**Health Check Automation**:
```bash
# Render pings this every 30 seconds
curl https://elicitron-backend.onrender.com/api/health

# Expected response:
{
  "status": "healthy",
  "version": "2.0.0",
  "timestamp": "2024-01-15T12:34:56.789Z",
  "service": "elicitron-backend"
}

# If unhealthy, Render auto-restarts service
```

**Set Up Alerts** (Render Dashboard):
1. Go to Service Settings
2. Add notification email
3. Get alerts for:
   - Service down
   - High error rate  
   - Memory limit reached

### Cost Breakdown

| Tier | Plan | Cost | Agents | Features |
|------|------|------|--------|----------|
| **Free** | Starter | $0/mo | 1-10 | Auto-scaling, 512MB RAM, cold starts |
| **Growth** | Standard | $25/mo | 10-50 | Always-on, 2GB RAM, auto-scale |
| **Scale** | Pro | $85/mo | 50+ | Multi-instance, 4GB RAM, priority support |

**Add-ons** (optional):
- Redis (free tier): Queue system for background jobs
- PostgreSQL (free tier): 1GB storage for job history
- Custom domain: Included in all plans

---

## 🐛 Troubleshooting

**Backend not starting?**
```bash
# Check Render logs
# Common issues:
# 1. Missing GOOGLE_API_KEY env var
# 2. requirements.txt missing dependencies
# 3. Port binding (use $PORT, not hardcoded 8000)
```

**Frontend can't reach backend?**
```bash
# Verify REACT_APP_API_URL in .env.production
# Check browser console for CORS errors
# Ensure backend CORS allows frontend domain
```

**Analysis timing out?**
```bash
# Should NOT timeout on Render (no 10s limit)
# If it does:
# 1. Check Render logs for Gemini API errors
# 2. Verify API key is valid
# 3. Monitor RAM usage (may need upgrade)
# 4. Check Gemini API quota (20 requests/min free tier)
```

**Cold starts too slow?**
```bash
# Free tier sleeps after 15 min inactivity
# Solutions:
# 1. Upgrade to Standard plan ($25/mo - always on)
# 2. Use cron-job.org to ping health endpoint every 14 min
# 3. Accept cold starts for demo (30s startup)
```

**API Quota Exceeded (429 Error):**
- Free tier: 20 requests/minute
- Solution: Wait for reset or upgrade to paid tier
- Workaround: Reduce `n_agents` parameter

**CORS Errors:**
- Check `allow_origins` in `app_fastapi.py`
- For production, specify exact frontend URL

**Docker Build Fails:**
- Clear Docker cache: `docker-compose down -v`
- Rebuild: `docker-compose up --build`

**React Proxy Not Working:**
- Verify `proxy` in `package.json` matches backend URL
- Check backend is running on port 8000

## 📚 API Documentation

- **Swagger UI:** http://localhost:8000/docs (interactive, try-it-out)
- **ReDoc:** http://localhost:8000/redoc (clean, printable)
- **OpenAPI Schema:** http://localhost:8000/openapi.json

**Production API Docs:**
- **Swagger UI:** https://elicitron-backend.onrender.com/docs
- **ReDoc:** https://elicitron-backend.onrender.com/redoc

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Inspired by the Elicitron methodology for requirements elicitation
- Powered by Google's Gemini AI
- Built with FastAPI and React modern web stack

## 📞 Support

- **GitHub Issues:** https://github.com/AashutoshAgrawal/product-requirements-simulator/issues
- **Documentation:** https://elicitron-backend.onrender.com/docs
- **Render Dashboard:** https://dashboard.render.com

## 🚀 Deployment Checklist

Before going live:
- ✅ Push all code to GitHub
- ✅ Add `GOOGLE_API_KEY` to Render environment variables
- ✅ Verify health check endpoint returns 200
- ✅ Test with 1 agent (quick smoke test)
- ✅ Test with 5 agents (full analysis)
- ✅ Monitor Render logs for errors
- ✅ Set up email alerts in Render dashboard
- ✅ Document backend URL for frontend config

**Success Criteria:**
- Backend health check: ✅ 200 OK
- Frontend loads: ✅ < 2 seconds
- Analysis completes: ✅ No timeout (152s+)
- Progress bar: ✅ Real-time updates
- Results display: ✅ Correctly formatted
- Auto-scaling: ✅ Configured

---

**Built with ❤️ for designers and product managers** | FastAPI + React | 2025

