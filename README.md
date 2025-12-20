# Requirements Elicitation Pipeline

A production-grade Python system that replicates the Elicitron-style requirements-elicitation pipeline using Google's Gemini as the LLM backend.

## 🎯 Purpose

This system automates the requirements elicitation process through:

1. **Agent Generation** - Serial generation of diverse user personas
2. **Experience Simulation** - Simulating user interactions (Action/Observation/Challenge)
3. **Interview Simulation** - Structured interviews based on simulated experiences
4. **Latent Need Extraction** - Classification and extraction of underlying user needs

## 🏗️ Architecture

```
product-requirements-simulator/
│
├── src/
│   ├── llm/                      # LLM Integration Layer
│   │   ├── gemini_client.py      # Gemini API client
│   │   └── prompts/              # Prompt templates
│   │       ├── agent_generation.txt
│   │       ├── experience_simulation.txt
│   │       ├── interview.txt
│   │       └── latent_classifier.txt
│   │
│   ├── agents/                   # Agent Operations
│   │   ├── generator.py          # User persona generation
│   │   ├── simulator.py          # Experience simulation
│   │   ├── interviewer.py        # Interview conduction
│   │   └── latent_extractor.py   # Need extraction & classification
│   │
│   ├── pipeline/                 # Orchestration
│   │   └── pipeline.py           # End-to-end workflow
│   │
│   └── utils/                    # Utilities
│       ├── logger.py             # Logging configuration
│       └── json_parser.py        # Safe JSON parsing
│
├── config/                       # Configuration
│   ├── settings.yaml             # System settings
│   └── interview_questions.yaml  # Interview questions
│
├── tests/                        # Test Suite
│   ├── test_pipeline.py
│   ├── test_agents.py
│   └── test_latent_extraction.py
│
├── main.py                       # Main entry point
├── requirements.txt              # Dependencies
├── .env.example                  # Environment template
└── README.md                     # This file
```

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Setup Steps

1. **Clone or download the repository**

```bash
cd product-requirements-simulator
```

2. **Create a virtual environment** (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Copy the example environment file and add your API key:

```bash
cp .env.example .env
```

Edit `.env` and replace `your_gemini_api_key_here` with your actual Gemini API key:

```
GOOGLE_API_KEY=your_actual_api_key_here
```

## 🚀 Usage

### Basic Usage

Run the complete pipeline with default settings:

```bash
python main.py
```

This will:
- Generate 5 diverse user agents
- Simulate their experiences with a camping tent
- Conduct structured interviews
- Extract and classify latent needs
- Save results to `results/` directory

### Custom Configuration

Modify `config/settings.yaml` to customize:

```yaml
agent_generation:
  default_n_agents: 10              # Number of agents
  default_design_context: "smartwatch"  # Product context

experience_simulation:
  default_product: "smartwatch"     # Product name

llm:
  model_name: "gemini-1.5-pro"      # Model selection
  temperature: 0.8                  # Creativity level
```

### Custom Interview Questions

Edit `config/interview_questions.yaml` to modify interview questions:

```yaml
questions:
  - "What was the most challenging part of your experience?"
  - "How would you improve this product?"
  - "What surprised you during the interaction?"
```

### Programmatic Usage

```python
from src.llm.gemini_client import GeminiClient
from src.pipeline.pipeline import RequirementsPipeline

# Initialize
client = GeminiClient(model_name="gemini-1.5-flash")
pipeline = RequirementsPipeline(client, questions=["Your question?"])

# Run pipeline
results = pipeline.run(
    n_agents=3,
    design_context="mobile app",
    product="fitness tracker"
)

# Access results
print(f"Extracted {results['aggregated_needs']['total_needs']} needs")
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_pipeline.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## 📊 Output Structure

The pipeline generates comprehensive results in JSON format:

```json
{
  "metadata": {
    "start_time": "2025-12-20T10:30:00",
    "n_agents": 5,
    "design_context": "camping tent",
    "duration_seconds": 45.2
  },
  "agents": ["agent descriptions..."],
  "experiences": [{"agent_id": 1, "experience": "..."}],
  "interviews": [{"agent_id": 1, "interview": [...]}],
  "aggregated_needs": {
    "total_needs": 23,
    "categories": {
      "Functional": [...],
      "Usability": [...]
    },
    "priorities": {
      "High": [...],
      "Medium": [...]
    }
  }
}
```

## 🔧 Advanced Features

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

Modify templates in `src/llm/prompts/` to customize LLM behavior:

- `agent_generation.txt` - How agents are created
- `experience_simulation.txt` - Experience structure
- `interview.txt` - Interview format
- `latent_classifier.txt` - Need extraction criteria

### Logging Configuration

Adjust logging in `config/settings.yaml`:

```yaml
logging:
  level: "DEBUG"  # DEBUG, INFO, WARNING, ERROR
  log_file: "pipeline.log"  # Optional file output
```

## 🛠️ Development

### Project Structure Philosophy

- **Modular Design**: Each component has a single responsibility
- **Clean Interfaces**: Components communicate through well-defined APIs
- **LLM Abstraction**: Only `gemini_client.py` knows about the LLM provider
- **Testability**: All components are independently testable

### Adding New Features

1. **New Agent Type**: Modify `agent_generation.txt` prompt template
2. **New Need Category**: Update `latent_classifier.txt` and `settings.yaml`
3. **New Interview Format**: Extend `Interviewer` class in `interviewer.py`

## 📝 Configuration Files

### settings.yaml

Global configuration for all pipeline components:
- LLM settings (model, temperature, retries)
- Default values for generation
- Need extraction categories
- Output preferences

### interview_questions.yaml

Interview question sets:
- Default questions list
- Categorized questions (usability, satisfaction, improvement)
- Custom question sets for specific contexts

## 🤝 Contributing

To contribute to this project:

1. Ensure all tests pass: `pytest tests/`
2. Add tests for new features
3. Follow existing code style and documentation patterns
4. Update README with new features

## 📄 License

This project is provided as-is for educational and research purposes.

## 🙏 Acknowledgments

Inspired by the Elicitron requirements elicitation methodology and powered by Google's Gemini AI.

## 📞 Support

For issues, questions, or contributions, please refer to the project repository or documentation.

---

**Note**: Always keep your `.env` file private and never commit API keys to version control.
A lightweight framework that uses AI agents to simulate user interviews and generate product requirements automatically. It helps teams explore user needs, uncover hidden pain points, and speed up early-stage product discovery.
