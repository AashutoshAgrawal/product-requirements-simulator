# Quick Start: Using OpenAI or Gemini

## 1. Install OpenAI Package
```bash
pip install openai==1.58.1
```

## 2. Set API Keys

### Option A: Use OpenAI
```bash
export OPENAI_API_KEY_1="sk-..."
```

### Option B: Use Gemini (existing)
```bash
export GOOGLE_API_KEY_1="AIza..."
```

## 3. Configure Provider

Edit `config/settings.yaml`:

### For OpenAI:
```yaml
llm:
  provider: "openai"
  model_name: "gpt-4o-mini"  # or gpt-4o, gpt-3.5-turbo
  temperature: 0.7
  rate_limit_delay: 0
```

### For Gemini:
```yaml
llm:
  provider: "gemini"
  model_name: "gemini-2.5-flash"  # or gemini-1.5-pro
  temperature: 0.7
  rate_limit_delay: 13
```

## 4. Run Application
```bash
python main.py
```

That's it! 🚀

---

## Where to Find Gemini Code

All Gemini-specific code is marked with `# GEMINI:` comments:

- [config/api_keys.py](config/api_keys.py) - Lines with `# GEMINI:`
- [src/llm/gemini_client.py](src/llm/gemini_client.py) - Entire file is Gemini
- [main.py](main.py) - Lines marked `# GEMINI:`
- [app_fastapi.py](app_fastapi.py) - Lines marked `# GEMINI:`

## Multiple API Keys (Load Balancing)

Both providers support multiple keys:

```bash
# OpenAI
export OPENAI_API_KEY_1="sk-..."
export OPENAI_API_KEY_2="sk-..."

# Gemini
export GOOGLE_API_KEY_1="AIza..."
export GOOGLE_API_KEY_2="AIza..."
```

Keys are automatically load-balanced across agents!
