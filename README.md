# Elicitron - AI-Powered Requirements Elicitation

A production-grade **FastAPI + React** full-stack web application that automates requirements elicitation using the Elicitron methodology with AI-powered simulation.

**Live Demo:**
- 🚀 **Frontend**: https://product-requirements-simulator.vercel.app
- 🔧 **Backend**: https://elicitron-backend.onrender.com

## 🎯 What is Elicitron?

Elicitron automates the requirements elicitation process through AI-powered simulation:

1. **Agent Generation** - Creates diverse user personas with varied backgrounds and needs
2. **Experience Simulation** - Simulates realistic user interactions (Action/Observation/Challenge)
3. **Interview Simulation** - Conducts structured follow-up interviews
4. **Latent Need Extraction** - Extracts, classifies, and prioritizes underlying user needs

**Perfect for:** Product managers, UX researchers, and development teams who need to understand user needs quickly without conducting dozens of real interviews.

## 🏗️ Tech Stack

**Backend:**
- FastAPI 0.115.0 (modern async Python web framework)
- OpenAI GPT-4o-mini (default LLM)
- Uvicorn (high-performance ASGI server)
- Pydantic (type-safe data validation)

**Frontend:**
- React 18.3.1 with TypeScript
- Shadcn/UI + Tailwind CSS
- Axios (HTTP client)

**Deployment:**
- Backend: Render.com (auto-scaling)
- Frontend: Vercel (edge network)
- Docker & Docker Compose support

## 📦 Quick Start

### Option 1: Docker (Recommended)

**Prerequisites:**
- Docker & Docker Compose installed
- OpenAI API key ([Get one](https://platform.openai.com/api-keys))

**Steps:**

```bash
# 1. Clone the repository
git clone https://github.com/AashutoshAgrawal/product-requirements-simulator.git
cd product-requirements-simulator

# 2. Set up environment variables
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=your_key_here

# 3. Start both backend and frontend
docker-compose up --build

# 4. Open your browser
# Frontend: http://localhost:3000
# Backend API Docs: http://localhost:8000/docs
```

### Option 2: Manual Setup (Development)

**Prerequisites:**
- Python 3.8+
- Node.js 14+ and npm
- OpenAI API key

**Backend Setup:**

```bash
# 1. Clone and navigate to project
git clone https://github.com/AashutoshAgrawal/product-requirements-simulator.git
cd product-requirements-simulator

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=your_key_here

# 5. Start FastAPI backend
python3 app_fastapi.py
# Backend runs at: http://localhost:8000
```

**Frontend Setup (separate terminal):**

```bash
# 1. Navigate to frontend directory
cd react-frontend

# 2. Install dependencies
npm install

# 3. Start React development server
npm start
# Frontend runs at: http://localhost:3000
```

## ⚙️ Configuration

### LLM Provider

Configure the OpenAI model in `config/settings.yaml`:

```yaml
llm:
  provider: "openai"
  model_name: "gpt-4o-mini"  # Options: "gpt-4o-mini", "gpt-4o"
  temperature: 0.0  # Lower = more deterministic
  seed: 42  # For reproducible OpenAI outputs
```

### API Keys

**OpenAI (current default):**
```bash
OPENAI_API_KEY=your_openai_key
# For scale, add more keys:
OPENAI_API_KEY_1=key1
OPENAI_API_KEY_2=key2
```

### System Configuration

Edit `config/settings.yaml`:

```yaml
agent_generation:
  default_n_agents: 1
  default_design_context: "smartwatch"

experience_simulation:
  default_product: "smartwatch"

need_extraction:
  categories:
    - Functional
    - Usability
    - Performance
    - Safety
    - Emotional
    - Social
    - Accessibility
```

### Interview Questions

Customize in `config/interview_questions.yaml`:

```yaml
questions:
  - "What was the most challenging part of your experience with this product?"
  - "If you could change one thing about this product to better fit your needs, what would it be and why?"
```

## 🚀 Usage

### Web Interface

1. Open http://localhost:3000 or the live demo
2. Enter product details (design context, product name, number of agents)
3. Click "Start Analysis"
4. Monitor real-time progress
5. View results organized by need categories
6. Download JSON for further analysis

### API Usage

```python
import requests

# Submit analysis job
response = requests.post("http://localhost:8000/api/analyze", json={
    "design_context": "smart fitness watch",
    "product": "smartwatch",
    "n_agents": 5,
    "pipeline_mode": "sequential"  # or "parallel"
})
job_id = response.json()["job_id"]

# Check status
status = requests.get(f"http://localhost:8000/api/status/{job_id}")
print(status.json())

# Get results
results = requests.get(f"http://localhost:8000/api/results/{job_id}")
print(f"Found {results.json()['aggregated_needs']['total_needs']} needs")
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/analyze` | POST | Submit new analysis job |
| `/api/status/{job_id}` | GET | Check job progress |
| `/api/results/{job_id}` | GET | Retrieve completed results |
| `/api/runs` | GET | List saved pipeline runs |
| `/api/health` | GET | Health check |

### CLI Usage

```bash
python main.py
# Results saved to: results/pipeline_results_TIMESTAMP.json
```

## 📊 Project Structure

```
product-requirements-simulator/
├── app_fastapi.py                # FastAPI backend (main production API)
├── main.py                       # CLI entry point
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Backend container
├── docker-compose.yml            # Multi-container orchestration
├── config/                       # Configuration
│   ├── settings.yaml            # System settings
│   ├── api_keys.py              # API key management
│   └── interview_questions.yaml
├── src/                          # Core Pipeline Logic
│   ├── llm/                     # LLM client (OpenAI)
│   ├── agents/                  # Generator, Simulator, Interviewer, Extractor
│   ├── pipeline/                 # Sequential & parallel pipelines
│   └── utils/                   # Analytics, logging, JSON parsing
├── react-frontend/               # React Frontend
│   └── src/figma-ui/           # UI components
└── tests/                       # Test Suite
```

## 📊 Understanding Results

### Need Categories

- **Functional**: Core product capabilities and features
- **Usability**: Ease of use, setup, learning curve
- **Performance**: Speed, reliability, efficiency
- **Safety**: Security, risk mitigation, trust
- **Emotional**: User feelings, confidence, satisfaction
- **Social**: Status, belonging, communication
- **Accessibility**: Inclusion, adaptation to diverse abilities

### Priority Levels

- **High**: Critical needs that must be addressed
- **Medium**: Important needs that enhance the product
- **Low**: Nice-to-have improvements

## 🧪 Testing

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## 🚢 Deployment

### Backend (Render.com)

1. Push code to GitHub
2. Connect repo to Render.com
3. Use render.yaml (auto-detected)
4. Add environment variables:
   - `OPENAI_API_KEY`

### Frontend (Vercel)

1. Connect GitHub repo to Vercel
2. Set root directory: `react-frontend`
3. Build command: `npm run build`
4. Add environment variable: `REACT_APP_API_URL`

## 🔧 Advanced Features

### Parallel Pipeline Mode

```python
# Use parallel mode for faster processing
response = requests.post("http://localhost:8000/api/analyze", json={
    "design_context": "smart fitness watch",
    "product": "smartwatch",
    "n_agents": 5,
    "pipeline_mode": "parallel"  # Faster but may hit rate limits
})
```

### Reproducibility Testing

Run the same analysis multiple times to measure consistency:

```python
# Via API
response = requests.post("http://localhost:8000/api/reproducibility/test", json={
    "product": "camping tent",
    "design_context": "ultralight backpacking",
    "n_agents": 3,
    "n_iterations": 3
})
```

### Programmatic Usage

```python
from src.llm.factory import create_llm_client
from src.pipeline.pipeline import RequirementsPipeline

# Initialize from config
import yaml
with open("config/settings.yaml") as f:
    config = yaml.safe_load(f)

llm_client = create_llm_client(config)
pipeline = RequirementsPipeline(llm_client, interview_questions=[])

results = pipeline.run(
    n_agents=5,
    design_context="smart home thermostat",
    product="thermostat"
)
```

### Custom Prompt Templates

Modify templates in `src/llm/prompts/`:

- `agent_generation.txt` - User persona generation
- `experience_simulation.txt` - Action/Observation/Challenge format
- `interview.txt` - Interview follow-up process
- `latent_classifier.txt` - Need extraction and categorization
- `need_synthesis.txt` - Deduplication of needs

## ⏱️ Performance

| Agents | Approximate Time |
|--------|-----------------|
| 1      | ~30 seconds     |
| 5      | ~3 minutes      |
| 10     | ~6 minutes      |

## 🐛 Troubleshooting

**"API key not found" error:**
```bash
# Check .env file
cat .env | grep OPENAI_API_KEY
```

**"Port 8000 already in use":**
```bash
lsof -ti:8000 | xargs kill -9
```

**Frontend can't connect to backend:**
```bash
curl http://localhost:8000/api/health
```

**Docker issues:**
```bash
docker-compose down -v
docker-compose up --build
```

## 📄 License

This project is provided as-is for educational and research purposes.

## 🙏 Acknowledgments

- **Methodology**: Inspired by the Elicitron requirements elicitation research
- **AI Models**: OpenAI GPT-4o-mini
- **Frameworks**: FastAPI and React

---

*Built for product teams who want to understand their users better, faster.*

