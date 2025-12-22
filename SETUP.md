# 🚀 Complete Setup Guide for New Systems

This guide walks you through setting up the Elicitron Requirements Elicitation system on a fresh machine.

## 📋 Prerequisites Checklist

Before you begin, ensure you have:

- [ ] **Operating System**: macOS, Linux, or Windows 10/11
- [ ] **Python**: Version 3.8 or higher ([Download](https://www.python.org/downloads/))
- [ ] **Node.js**: Version 14 or higher ([Download](https://nodejs.org/))
- [ ] **Git**: For cloning the repository ([Download](https://git-scm.com/))
- [ ] **Google Gemini API Key**: Free tier available ([Get one](https://aistudio.google.com/app/apikey))
- [ ] **Text Editor**: VS Code, PyCharm, or your preferred editor

**Optional but Recommended:**
- [ ] **Docker Desktop**: For containerized deployment ([Download](https://www.docker.com/products/docker-desktop/))
- [ ] **GitHub Account**: For deploying to production

---

## 🎯 Method 1: Docker Setup (Easiest)

**Best for:** Quick start, consistent environment, production-like setup

### Step 1: Install Docker

**macOS:**
```bash
# Download and install Docker Desktop from:
# https://www.docker.com/products/docker-desktop/

# Verify installation
docker --version
docker-compose --version
```

**Linux (Ubuntu/Debian):**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt-get install docker-compose

# Add user to docker group (optional, avoids sudo)
sudo usermod -aG docker $USER
newgrp docker
```

**Windows:**
- Download Docker Desktop from https://www.docker.com/products/docker-desktop/
- Follow installation wizard
- Enable WSL 2 backend if prompted

### Step 2: Clone Repository

```bash
# Clone the repository
git clone https://github.com/AashutoshAgrawal/product-requirements-simulator.git

# Navigate to directory
cd product-requirements-simulator
```

### Step 3: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your API key
# On macOS/Linux:
nano .env

# On Windows:
notepad .env

# Add your API key:
# GOOGLE_API_KEY=your_actual_api_key_here
```

### Step 4: Start Application

```bash
# Build and start both backend and frontend
docker-compose up --build

# This will:
# - Build backend Docker image
# - Build frontend Docker image with nginx
# - Start backend on http://localhost:8000
# - Start frontend on http://localhost:3000
```

### Step 5: Access Application

Open your browser:
- **Frontend UI**: http://localhost:3000
- **Backend API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

### Step 6: Test the System

1. Open http://localhost:3000
2. Enter:
   - Design Context: "camping tent"
   - Product: "tent"
   - Number of Agents: 2 (for quick test)
3. Click "Start Analysis"
4. Watch real-time progress (~2 minutes)
5. View and download results

**To stop:**
```bash
# Press Ctrl+C in terminal, then:
docker-compose down
```

---

## 🔧 Method 2: Manual Setup (Development)

**Best for:** Development, customization, debugging

### Step 1: Install Python

**Verify Python version:**
```bash
python3 --version
# Should show Python 3.8 or higher
```

**If not installed:**
- **macOS**: `brew install python@3.11` (requires Homebrew)
- **Linux**: `sudo apt-get install python3.11`
- **Windows**: Download from https://www.python.org/downloads/

### Step 2: Install Node.js

**Verify Node version:**
```bash
node --version
npm --version
# Node should be 14+ and npm should be 6+
```

**If not installed:**
- **macOS**: `brew install node`
- **Linux**: `sudo apt-get install nodejs npm`
- **Windows**: Download from https://nodejs.org/

### Step 3: Clone and Setup Backend

```bash
# Clone repository
git clone https://github.com/AashutoshAgrawal/product-requirements-simulator.git
cd product-requirements-simulator

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# Verify activation (should show (venv) in prompt)

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# This installs:
# - FastAPI & Uvicorn (web framework)
# - Google Generative AI (Gemini)
# - Pydantic (data validation)
# - pytest (testing)
# - and other dependencies
```

### Step 4: Configure Environment Variables

```bash
# Copy example file
cp .env.example .env

# Edit with your preferred editor
# macOS/Linux:
nano .env
# or
vim .env
# or
code .env  # if using VS Code

# Windows:
notepad .env

# Required: Add your Gemini API key
# GOOGLE_API_KEY=your_key_here

# Optional: Add multiple keys for scaling
# GOOGLE_API_KEY_1=first_key
# GOOGLE_API_KEY_2=second_key
```

**Get your API key:**
1. Visit https://aistudio.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key and paste it in `.env`

### Step 5: Test Backend

```bash
# Make sure virtual environment is active
# Should see (venv) in prompt

# Start FastAPI server
python3 app_fastapi.py

# You should see:
# INFO:     Started server process
# INFO:     Uvicorn running on http://0.0.0.0:8000

# Test in another terminal:
curl http://localhost:8000/api/health
# Should return: {"status":"healthy","timestamp":"..."}
```

### Step 6: Setup Frontend

**Open a NEW terminal (keep backend running):**

```bash
# Navigate to frontend directory
cd product-requirements-simulator/react-frontend

# Install Node dependencies
npm install

# This installs:
# - React & React DOM
# - Axios (HTTP client)
# - React Scripts (development tools)

# Start development server
npm start

# This will:
# - Compile React app
# - Open browser automatically at http://localhost:3000
# - Enable hot reloading (changes appear instantly)
```

### Step 7: Verify Everything Works

**You should now have:**
- ✅ Backend running on http://localhost:8000
- ✅ Frontend running on http://localhost:3000
- ✅ Auto-opened browser window showing the UI

**Test the full flow:**
1. In browser at http://localhost:3000
2. Enter test data:
   - Design Context: "smart watch"
   - Product: "watch"
   - Agents: 1 (quick test)
3. Click "Start Analysis"
4. Monitor progress in UI
5. View results when complete

**Check backend logs:**
- Terminal running `app_fastapi.py` shows request logs
- Look for: POST /api/analyze, GET /api/status, GET /api/results

---

## 🧪 Verify Installation

### Backend Tests

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run all tests
pytest tests/ -v

# Expected output:
# test_agent_generation.py ✓
# test_pipeline.py ✓
# test_latent_extraction.py ✓
# All tests passed!

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing

# Should show >80% coverage
```

### API Tests

```bash
# Test health endpoint
curl http://localhost:8000/api/health

# Should return:
# {"status":"healthy","timestamp":"2025-12-21T..."}

# Test API docs (open in browser)
open http://localhost:8000/docs  # macOS
# or just visit http://localhost:8000/docs in browser
```

### Frontend Tests

```bash
cd react-frontend

# Run React tests
npm test

# Should show: All tests passed
```

---

## 🔍 Troubleshooting

### Problem: "Python not found" or "python3: command not found"

**Solution:**
```bash
# Check if Python is installed
which python3
python3 --version

# If not installed, install Python 3.8+
# macOS: brew install python@3.11
# Linux: sudo apt-get install python3.11
# Windows: Download from python.org
```

### Problem: "pip: command not found"

**Solution:**
```bash
# Use python3 -m pip instead
python3 -m pip install -r requirements.txt

# Or install pip
python3 -m ensurepip --upgrade
```

### Problem: "Permission denied" when installing packages

**Solution:**
```bash
# Use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Or use --user flag (not recommended)
pip install --user -r requirements.txt
```

### Problem: "Port 8000 already in use"

**Solution:**
```bash
# Find process using port 8000
# macOS/Linux:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different port
uvicorn app_fastapi:app --port 8001
```

### Problem: "npm: command not found"

**Solution:**
```bash
# Install Node.js which includes npm
# macOS: brew install node
# Linux: sudo apt-get install nodejs npm
# Windows: Download from nodejs.org

# Verify installation
node --version
npm --version
```

### Problem: "API key not found" error

**Solution:**
```bash
# Check .env file exists
ls -la .env

# Check contents
cat .env | grep GOOGLE_API_KEY

# Should show: GOOGLE_API_KEY=AIza...
# If empty, add your key:
echo "GOOGLE_API_KEY=your_key_here" > .env

# Restart backend after adding key
```

### Problem: Frontend can't connect to backend (CORS errors)

**Solution:**
1. Verify backend is running: `curl http://localhost:8000/api/health`
2. Check CORS is enabled in `app_fastapi.py` (it should be)
3. Verify frontend is using correct API URL
4. Clear browser cache and refresh

### Problem: "Module not found" errors

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# If still failing, delete and recreate venv
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Problem: Docker "Cannot connect to Docker daemon"

**Solution:**
```bash
# Make sure Docker Desktop is running
# On macOS: Look for Docker icon in menu bar
# On Windows: Check system tray

# Start Docker service on Linux
sudo systemctl start docker

# Check Docker status
docker info
```

---

## 📁 File Structure After Setup

```
product-requirements-simulator/
├── venv/                          # Virtual environment (if manual setup)
├── node_modules/                  # Node packages (in react-frontend/)
├── .env                          # Your API keys (NOT in git)
├── .env.example                  # Template for .env
├── app_fastapi.py                # Backend entry point
├── main.py                       # CLI entry point
├── requirements.txt              # Python dependencies
├── src/                          # Core pipeline code
├── react-frontend/               # React frontend
│   ├── node_modules/            # Frontend dependencies
│   ├── src/                     # React components
│   └── package.json             # Frontend config
├── config/                       # Configuration files
├── tests/                        # Test suite
├── results/                      # Generated results (created on first run)
└── logs/                         # Log files (created on first run)
```

---

## 🎓 Next Steps

### Learn the System

1. **Read the methodology**: See `Elicitron Research Paper.pdf`
2. **Explore API docs**: http://localhost:8000/docs
3. **Try different products**: Test with various product types
4. **Customize prompts**: Edit files in `src/llm/prompts/`
5. **Review results**: Analyze JSON outputs in `results/` folder

### Customize Configuration

1. **Edit `config/settings.yaml`**: Adjust model, temperature, categories
2. **Edit `config/interview_questions.yaml`**: Add custom questions
3. **Add multiple API keys**: See `API_KEYS_SETUP.md`

### Deploy to Production

1. **Read `DEPLOYMENT.md`**: Complete deployment guide
2. **Push to GitHub**: Commit and push your code
3. **Deploy backend**: Use Render.com (free tier)
4. **Deploy frontend**: Use Vercel (free tier)

### Develop New Features

1. **Run tests**: `pytest tests/ -v`
2. **Add functionality**: Modify `src/` modules
3. **Write tests**: Add to `tests/` directory
4. **Update docs**: Keep README.md current

---

## 📞 Getting Help

**If you're stuck:**

1. **Check Troubleshooting section** above
2. **Review error messages** carefully
3. **Check logs**: Backend terminal and `logs/` directory
4. **Test each component** separately (backend, frontend, tests)
5. **Open an issue**: https://github.com/AashutoshAgrawal/product-requirements-simulator/issues

**Include in issue reports:**
- Operating system and version
- Python version (`python3 --version`)
- Node version (`node --version`)
- Complete error message
- Steps to reproduce

---

## ✅ Setup Verification Checklist

Before proceeding, verify:

- [ ] Backend starts without errors
- [ ] Frontend loads in browser
- [ ] Health check returns healthy status
- [ ] API docs accessible at /docs
- [ ] Test analysis completes successfully
- [ ] Results appear in UI
- [ ] JSON export works
- [ ] All tests pass with pytest
- [ ] No error messages in logs

**If all checked: Congratulations! Your system is ready to use! 🎉**

---

*Last updated: December 21, 2025*
