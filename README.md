# Elicitron - AI-Powered Requirements Elicitation

A production-grade **FastAPI + React** full-stack web application that automates requirements elicitation using the Elicitron methodology with Google's Gemini AI.

**Live Demo:**
- 🚀 **Frontend**: https://product-requirements-simulator.vercel.app
- 🔧 **Backend**: https://elicitron-backend.onrender.com

## 📖 Documentation

- **[⚡ QUICKSTART.md](QUICKSTART.md)** - Get running in 5 minutes
- **[🔧 SETUP.md](SETUP.md)** - Complete setup guide for new systems
- **[🚢 DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide
- **[🔑 API_KEYS_SETUP.md](API_KEYS_SETUP.md)** - API key configuration for scaling

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
- Google Gemini 2.5 Flash (LLM)
- Uvicorn (high-performance ASGI server)
- Pydantic (type-safe data validation)

**Frontend:**
- React 18.3.1
- Axios (HTTP client)
- Modern responsive UI with gradient design

**Deployment:**
- Backend: Render.com (auto-scaling)
- Frontend: Vercel (edge network)
- Docker & Docker Compose support

## 📦 Quick Start

> **💡 First time?** See [QUICKSTART.md](QUICKSTART.md) for the fastest path.
> 
> **🔧 Detailed setup?** See [SETUP.md](SETUP.md) for comprehensive instructions.

### Option 1: Docker (Recommended for New Systems)

**Prerequisites:**
- Docker & Docker Compose installed
- Google Gemini API key ([Get one free](https://aistudio.google.com/app/apikey))

**Steps:**

```bash
# 1. Clone the repository
git clone https://github.com/AashutoshAgrawal/product-requirements-simulator.git
cd product-requirements-simulator

# 2. Set up environment variables
cp .env.example .env
# Edit .env and add your API key: GOOGLE_API_KEY=your_key_here

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
- Google Gemini API key

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
# Edit .env and add: GOOGLE_API_KEY=your_key_here

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

## 🚀 Usage

### Web Interface (Primary Method)

1. **Open the app** in your browser (http://localhost:3000 or live demo)
2. **Enter product details:**
   - Design context (e.g., "camping tent", "fitness app")
   - Product name (e.g., "tent", "smartwatch")
   - Number of agents (1-50, recommended: 5-10)
3. **Click "Start Analysis"** - Processing takes 1-2 minutes per agent
4. **Monitor real-time progress** - See which stage is running
5. **View results** - Organized by need categories (Functional, Usability, Performance, etc.)
6. **Download JSON** - Export complete results for further analysis

### API Usage (Programmatic)

```python
import requests

# Submit analysis job
response = requests.post("http://localhost:8000/api/analyze", json={
    "design_context": "smart fitness watch",
    "product": "smartwatch",
    "n_agents": 5
})
job_id = response.json()["job_id"]

# Check status
status = requests.get(f"http://localhost:8000/api/status/{job_id}")
print(status.json())  # Shows progress: generating_agents, simulating_experiences, etc.

# Get results when complete
results = requests.get(f"http://localhost:8000/api/results/{job_id}")
print(f"Found {results.json()['aggregated_needs']['total_needs']} needs")
```

### CLI Usage (Legacy, Optional)

```bash
# Run complete pipeline from command line
python main.py

# Results saved to: results/pipeline_results_TIMESTAMP.json
```

## 📊 Project Structure

```
product-requirements-simulator/
│
├── app_fastapi.py                # 🚀 FastAPI backend (main production API)
├── main.py                       # 🖥️ CLI entry point (optional)
├── requirements.txt              # 📦 Python dependencies
├── Dockerfile                    # 🐳 Backend container
├── docker-compose.yml            # 🎼 Multi-container orchestration
│
├── react-frontend/               # ⚛️ React Frontend
│   ├── src/
│   │   ├── App.jsx              # Main UI component
│   │   ├── App.css              # Styling
│   │   └── index.js             # Entry point
│   ├── package.json             # Node dependencies
│   ├── Dockerfile               # Frontend container (nginx)
│   └── nginx.conf               # Reverse proxy config
│
├── src/                          # 🧠 Core Pipeline Logic
│   ├── llm/
│   │   ├── gemini_client.py     # Gemini API client
│   │   └── prompts/             # LLM prompt templates
│   ├── agents/
│   │   ├── generator.py         # User persona generation
│   │   ├── simulator.py         # Experience simulation
│   │   ├── interviewer.py       # Interview conduction
│   │   └── latent_extractor.py  # Need extraction
│   ├── pipeline/
│   │   └── pipeline.py          # Orchestration
│   └── utils/
│       ├── logger.py            # Logging
│       └── json_parser.py       # JSON parsing
│
├── config/                       # ⚙️ Configuration
│   ├── settings.yaml            # System settings
│   └── interview_questions.yaml # Interview templates
│
├── tests/                        # 🧪 Test Suite
│   ├── test_pipeline.py
│   ├── test_agents.py
│   └── test_latent_extraction.py
│
├── DEPLOYMENT.md                 # 🚢 Production deployment guide
├── API_KEYS_SETUP.md            # 🔑 API key configuration
└── README.md                    # 📖 This file
```

## ⚙️ Configuration

### API Keys for Scale

For processing many agents (10+), you can add multiple API keys for load balancing:

**See [API_KEYS_SETUP.md](API_KEYS_SETUP.md) for detailed instructions.**

Quick setup in `.env`:
```bash
GOOGLE_API_KEY_1=your_first_key
GOOGLE_API_KEY_2=your_second_key
GOOGLE_API_KEY_3=your_third_key
# The system automatically detects and load-balances across all keys
```

### System Configuration

Edit `config/settings.yaml` to customize pipeline behavior:

```yaml
agent_generation:
  default_n_agents: 10              # Number of agents to generate
  default_design_context: "smartwatch"  # Default product context

experience_simulation:
  default_product: "smartwatch"     # Default product name

llm:
  model_name: "gemini-1.5-flash"   # Gemini model (flash = faster, pro = better)
  temperature: 0.7                  # Creativity (0.0-1.0, higher = more creative)
  max_retries: 3                    # Retry failed API calls

need_extraction:
  categories:                        # Need categories for classification
    - Functional
    - Usability
    - Performance
    - Safety
    - Emotional
```

### Interview Questions

Customize interview questions in `config/interview_questions.yaml`:

```yaml
questions:
  - "What was the most challenging part of your experience with this product?"
  - "If you could change one thing about this product to better fit your needs, what would it be and why?"
  # Add your own questions here
```

## 📊 Understanding the Results

### Output Format

Results are saved as JSON with comprehensive metadata:

```json
{
  "metadata": {
    "start_time": "2025-12-20T10:30:00",
    "end_time": "2025-12-20T10:36:30",
    "duration_seconds": 152.3,
    "n_agents": 5,
    "design_context": "camping tent",
    "product": "tent",
    "status": "completed"
  },
  "agents": [
    "**Name**: Alex, Ultralight Backpacker\n**Description**: Experienced hiker...",
    // ... more agents
  ],
  "experiences": [
    {
      "agent_id": 1,
      "agent": "Alex, Ultralight Backpacker",
      "experience": "**Step 1:** Action... Observation... Challenge..."
    }
  ],
  "interviews": [
    {
      "agent_id": 1,
      "interview": [
        {
          "question": "What was most challenging?",
          "answer": "The condensation management..."
        }
      ]
    }
  ],
  "need_extractions": [
    {
      "agent_id": 1,
      "total_needs": 9,
      "needs": [
        {
          "category": "Functional",
          "need_statement": "User needs better ventilation...",
          "evidence": "Quote from interview...",
          "priority": "High",
          "design_implication": "Add larger vents..."
        }
      ]
    }
  ],
  "aggregated_needs": {
    "total_needs": 23,
    "total_agents": 5,
    "categories": {
      "Functional": [...],
      "Usability": [...],
      "Performance": [...],
      "Safety": [...],
      "Emotional": [...]
    }
  }
}
```

### Need Categories

- **Functional**: Core product capabilities and features
- **Usability**: Ease of use, setup, learning curve
- **Performance**: Speed, reliability, efficiency
- **Safety**: Security, risk mitigation, trust
- **Emotional**: User feelings, confidence, satisfaction

### Priority Levels

- **High**: Critical user needs that must be addressed
- **Medium**: Important needs that enhance the product
- **Low**: Nice-to-have improvements

## 🧪 Testing

Run the test suite to ensure everything works:

```bash
# Activate virtual environment first
source venv/bin/activate  # Windows: venv\Scripts\activate

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_pipeline.py -v

# Run with coverage report
pytest tests/ --cov=src --cov-report=html
# View coverage: open htmlcov/index.html
```

## 🚢 Deployment

### Deploy to Production

**See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment guide.**

Quick deployment to Render + Vercel (free tier):

```bash
# 1. Push code to GitHub
git add .
git commit -m "Ready for deployment"
git push origin main

# 2. Deploy backend to Render.com
# - Connect GitHub repo
# - Use render.yaml (auto-detected)
# - Add GOOGLE_API_KEY environment variable

# 3. Deploy frontend to Vercel
# - Connect GitHub repo
# - Root directory: react-frontend
# - Build command: npm run build
# - Add REACT_APP_API_URL environment variable

# Your app is live! 🎉
```

### Environment Variables for Production

**Backend (Render):**
- `GOOGLE_API_KEY_1` - Primary API key (required)
- `GOOGLE_API_KEY_2`, `GOOGLE_API_KEY_3`, etc. - Additional keys for scale (optional)

**Frontend (Vercel):**
- `REACT_APP_API_URL` - Backend URL (e.g., https://elicitron-backend.onrender.com)

## 🔧 Advanced Features

### Programmatic Usage (Python SDK)

```python
from src.llm.gemini_client import GeminiClient
from src.pipeline.pipeline import RequirementsPipeline

# Initialize with custom settings
client = GeminiClient(
    model_name="gemini-1.5-flash",
    temperature=0.7,
    max_retries=3
)

questions = [
    "What was the most challenging part of your experience?",
    "What would you change about this product?"
]

pipeline = RequirementsPipeline(
    llm_client=client,
    interview_questions=questions
)

# Run full pipeline
results = pipeline.run(
    n_agents=5,
    design_context="smart home thermostat",
    product="thermostat"
)

# Access specific results
print(f"Generated {len(results['agents'])} agents")
print(f"Extracted {results['aggregated_needs']['total_needs']} total needs")

# Filter high-priority functional needs
functional_needs = results['aggregated_needs']['categories'].get('Functional', [])
high_priority = [n for n in functional_needs if n['priority'] == 'High']
print(f"Found {len(high_priority)} high-priority functional needs")
```

### Partial Pipeline Execution

Run only specific stages:

```python
# Run only agent generation and experience simulation
results = pipeline.run_partial(
    start_stage="agents",
    end_stage="experiences",
    n_agents=3,
    design_context="smartphone"
)
```

### Custom Prompt Templates

Modify templates in `src/llm/prompts/` to customize AI behavior:

- **`agent_generation.txt`** - Controls how diverse user personas are created
- **`experience_simulation.txt`** - Defines the Action/Observation/Challenge format
- **`interview.txt`** - Structures the interview follow-up process
- **`latent_classifier.txt`** - Determines need extraction and categorization

Example: Edit `agent_generation.txt` to focus on specific user demographics or to emphasize certain aspects like technical expertise, budget constraints, etc.

### Logging Configuration

Adjust logging verbosity in `config/settings.yaml`:

```yaml
logging:
  level: "INFO"  # DEBUG for detailed logs, INFO for normal, WARNING for errors only
  log_file: "pipeline.log"  # Optional: save logs to file
```

Or configure programmatically:

```python
from src.utils.logger import configure_logging

configure_logging(level="DEBUG", log_file="my_pipeline.log")
```

## 🔍 API Documentation

When running the backend, visit these URLs for interactive API docs:

- **Swagger UI**: http://localhost:8000/docs
  - Interactive API testing interface
  - Try endpoints directly from browser
  
- **ReDoc**: http://localhost:8000/redoc
  - Clean, readable API documentation
  - Better for learning the API structure

### Main API Endpoints

```
POST   /api/analyze          - Submit new analysis job
GET    /api/status/{job_id}  - Check job progress
GET    /api/results/{job_id} - Retrieve completed results
GET    /api/health           - Health check endpoint
```

## ⏱️ Performance & Timing

**Expected processing times:**

| Agents | Approximate Time | Use Case |
|--------|-----------------|----------|
| 1      | ~60 seconds     | Quick testing |
| 5      | ~6 minutes      | Standard analysis |
| 10     | ~12 minutes     | Comprehensive study |
| 50     | ~60 minutes     | Enterprise research |

**Breakdown per agent (~1-2 minutes each):**
- Agent generation: ~12 seconds
- Experience simulation: ~12 seconds
- Interview (2 questions): ~24 seconds
- Need extraction: ~24 seconds

**Note:** Times include 12-second rate limiting between API calls to respect Gemini's usage limits.

## 🛠️ Development & Contributing

### Development Setup

```bash
# 1. Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/product-requirements-simulator.git
cd product-requirements-simulator

# 2. Set up Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Set up pre-commit hooks (optional but recommended)
pip install pre-commit
pre-commit install

# 4. Run tests to verify setup
pytest tests/ -v
```

### Project Architecture Philosophy

- **Modular Design**: Each component (agents, pipeline, LLM) has a single responsibility
- **Clean Interfaces**: Components communicate through well-defined APIs
- **LLM Abstraction**: Only `gemini_client.py` knows about the LLM provider (easy to swap)
- **Type Safety**: Pydantic models ensure data validation
- **Testability**: All components are independently testable
- **Async-First**: FastAPI enables non-blocking I/O for better performance

### Adding New Features

**1. New Agent Generation Strategy:**
- Modify `src/llm/prompts/agent_generation.txt`
- Adjust `src/agents/generator.py` if needed

**2. New Need Category:**
- Update `config/settings.yaml` → `need_extraction.categories`
- Update `src/llm/prompts/latent_classifier.txt` to recognize new category

**3. New Interview Question Set:**
- Create new YAML file in `config/` (e.g., `config/technical_questions.yaml`)
- Pass custom questions to pipeline:
  ```python
  pipeline = RequirementsPipeline(client, interview_questions=your_questions)
  ```

**4. New LLM Provider (e.g., OpenAI, Anthropic):**
- Create new client class in `src/llm/` (e.g., `openai_client.py`)
- Implement same interface as `GeminiClient`
- Update initialization in `app_fastapi.py` and `main.py`

### Code Style

- Follow PEP 8 for Python code
- Use type hints wherever possible
- Write docstrings for all classes and functions
- Keep functions focused and under 50 lines when possible
- Use meaningful variable names

### Testing Guidelines

```bash
# Run tests with coverage
pytest tests/ --cov=src --cov-report=term-missing

# Test specific module
pytest tests/test_agents.py -v

# Test with logging output
pytest tests/ -v -s

# Add new tests in tests/ directory following existing patterns
```

### Contributing Workflow

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes with tests
3. Ensure all tests pass: `pytest tests/ -v`
4. Update documentation if needed (README, docstrings)
5. Commit with clear messages: `git commit -m "Add: feature description"`
6. Push and create Pull Request

## 🐛 Troubleshooting

### Common Issues

**"API key not found" error:**
```bash
# Make sure .env file exists and has the key
cat .env | grep GOOGLE_API_KEY
# Should show: GOOGLE_API_KEY=your_key_here

# Restart the backend after adding the key
```

**"Port 8000 already in use":**
```bash
# Find and kill the process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn app_fastapi:app --port 8001
```

**"Module not found" errors:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**Frontend can't connect to backend:**
```bash
# Check backend is running
curl http://localhost:8000/api/health

# Check CORS is enabled (should be in app_fastapi.py)
# Verify frontend API URL matches backend URL
```

**Docker issues:**
```bash
# Rebuild containers from scratch
docker-compose down -v
docker-compose up --build

# Check container logs
docker-compose logs backend
docker-compose logs frontend
```

### Getting Help

- **Issues**: Open an issue on GitHub with detailed description
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check DEPLOYMENT.md and API_KEYS_SETUP.md for specific topics

## 📄 License

This project is provided as-is for educational and research purposes.

## 🙏 Acknowledgments

- **Methodology**: Inspired by the [Elicitron requirements elicitation research](./Elicitron%20Research%20Paper.pdf)
- **AI Model**: Powered by Google's Gemini AI
- **Framework**: Built with FastAPI and React
- **Community**: Thanks to all contributors and users providing feedback

## 📚 Additional Documentation

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Complete production deployment guide (Render, Vercel, Docker)
- **[API_KEYS_SETUP.md](API_KEYS_SETUP.md)** - Detailed API key configuration for scaling
- **API Docs** - Interactive docs at `/docs` and `/redoc` when backend is running

## 🎯 Use Cases

**Product Management:**
- Rapid user research for new product ideas
- Identify pain points without conducting dozens of interviews
- Validate feature priorities with simulated user feedback

**UX Research:**
- Generate diverse user personas automatically
- Explore edge cases and accessibility needs
- Supplement real user research with AI-simulated perspectives

**Startup Validation:**
- Test product-market fit hypotheses
- Understand user needs before building
- Generate requirements documentation quickly

**Education:**
- Teach requirements elicitation methodology
- Demonstrate AI applications in product development
- Practice analyzing user needs

## 📞 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/AashutoshAgrawal/product-requirements-simulator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/AashutoshAgrawal/product-requirements-simulator/discussions)
- **Email**: For private inquiries or collaboration opportunities

---

**⚠️ Security Note**: Always keep your `.env` file private and never commit API keys to version control. The `.gitignore` file is configured to protect your keys, but double-check before pushing to public repositories.

**🚀 Live Demo**: Try it now at https://product-requirements-simulator.vercel.app

---

*Built with ❤️ for product teams who want to understand their users better, faster.*
