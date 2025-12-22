# ⚡ Quick Start Guide

Get Elicitron running in 5 minutes!

## 🎯 Choose Your Path

### Path 1: Docker (Fastest) 🐳

```bash
# 1. Clone
git clone https://github.com/AashutoshAgrawal/product-requirements-simulator.git
cd product-requirements-simulator

# 2. Configure API Key
cp .env.example .env
# Edit .env and add: GOOGLE_API_KEY=your_key_from_aistudio.google.com

# 3. Start Everything
docker-compose up --build

# 4. Open Browser
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

**Done! 🎉** Try analyzing "camping tent" with 2 agents.

---

### Path 2: Manual (For Development) 💻

**Backend:**
```bash
# 1. Clone
git clone https://github.com/AashutoshAgrawal/product-requirements-simulator.git
cd product-requirements-simulator

# 2. Setup Python
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure
cp .env.example .env
# Edit .env and add your API key

# 4. Run
python3 app_fastapi.py
```

**Frontend (new terminal):**
```bash
cd react-frontend
npm install
npm start
```

**Done! 🎉** Browser opens automatically at http://localhost:3000

---

## 🔑 Get Your API Key

1. Visit: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key (starts with `AIza...`)
4. Paste in `.env` file

**Free tier limits:**
- 60 requests/minute
- 1500 requests/day
- Sufficient for testing and small-scale use

---

## 🧪 First Test

1. **Open**: http://localhost:3000
2. **Enter**:
   - Design Context: `camping tent`
   - Product: `tent`
   - Number of Agents: `2` (quick test)
3. **Click**: "Start Analysis"
4. **Wait**: ~2 minutes
5. **View**: Results with extracted user needs

---

## 📊 Example Results

After processing, you'll see:

- **Generated Agents**: 2 diverse user personas
- **Experiences**: Simulated product interactions
- **Interviews**: Follow-up Q&A
- **Extracted Needs**: Categorized by:
  - Functional
  - Usability
  - Performance
  - Safety
  - Emotional

**Download JSON** for detailed analysis.

---

## 🎓 Next Steps

**Learn More:**
- Full setup guide: [SETUP.md](SETUP.md)
- Deployment guide: [DEPLOYMENT.md](DEPLOYMENT.md)
- API docs: http://localhost:8000/docs

**Customize:**
- Edit prompts: `src/llm/prompts/`
- Change questions: `config/interview_questions.yaml`
- Adjust settings: `config/settings.yaml`

**Scale Up:**
- Add more API keys: [API_KEYS_SETUP.md](API_KEYS_SETUP.md)
- Test with 10+ agents
- Deploy to production

---

## 🐛 Quick Fixes

**Backend won't start?**
```bash
# Check Python version (need 3.8+)
python3 --version

# Reinstall dependencies
pip install -r requirements.txt

# Check API key
cat .env | grep GOOGLE_API_KEY
```

**Frontend won't start?**
```bash
# Check Node version (need 14+)
node --version

# Reinstall dependencies
cd react-frontend
rm -rf node_modules
npm install
```

**"Port already in use"?**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn app_fastapi:app --port 8001
```

---

## 📞 Need Help?

- **Full troubleshooting**: [SETUP.md](SETUP.md#troubleshooting)
- **GitHub Issues**: [Report a problem](https://github.com/AashutoshAgrawal/product-requirements-simulator/issues)
- **Documentation**: [README.md](README.md)

---

**Ready? Let's go! 🚀**

```bash
docker-compose up --build
```

*Takes 2-3 minutes first time to build images. Subsequent starts are instant!*
