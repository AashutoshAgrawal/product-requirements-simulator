# 🔑 API Key Setup Guide

## For Multiple Agents & Scaling

This application supports **multiple API keys** for load balancing across many agents, preventing rate limits and timeouts.

---

## 📍 Local Development

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Add your API keys to `.env`:**
   ```bash
   GOOGLE_API_KEY_1=your_first_api_key_here
   GOOGLE_API_KEY_2=your_second_api_key_here
   GOOGLE_API_KEY_3=your_third_api_key_here
   # Add more as needed...
   ```

3. **The system will automatically:**
   - Load all numbered keys (`GOOGLE_API_KEY_1`, `GOOGLE_API_KEY_2`, etc.)
   - Distribute requests across keys using load balancing
   - Track usage and prevent rate limits

---

## 🚀 Production (Render.com)

### Setting Up Multiple API Keys on Render:

1. **Go to your Render Dashboard:**
   - Navigate to: https://dashboard.render.com/
   - Click on your `elicitron-backend` service

2. **Add Environment Variables:**
   - Click **"Environment"** in the left sidebar
   - Click **"Add Environment Variable"** button
   - Add each key individually:

   ```
   Key: GOOGLE_API_KEY_1
   Value: AIzaSyC1HBVK2XY-gebCyE6N77q6IsklqMRRfxY

   Key: GOOGLE_API_KEY_2
   Value: your_second_key_here

   Key: GOOGLE_API_KEY_3
   Value: your_third_key_here

   ... (add as many as you need)
   ```

3. **Save Changes:**
   - Click **"Save Changes"**
   - Render will automatically redeploy with the new keys
   - Check logs to confirm: `✅ Loaded N API key(s) from environment`

---

## 📈 Scaling to 50+ Agents

The system is designed to handle many agents:

1. **Get more API keys:**
   - Visit: https://makersuite.google.com/app/apikey
   - Create additional keys for your project

2. **Add them to Render:**
   - Continue numbering: `GOOGLE_API_KEY_4`, `GOOGLE_API_KEY_5`, etc.
   - The system automatically detects and uses all numbered keys

3. **Load Balancing Strategies:**
   - **Round-robin** (default): Cycles through keys sequentially
   - **Random**: Picks a random key for each request
   - **Least-used**: Uses the key with fewest requests

---

## 🔒 Security

✅ **Keys are SECURE:**
- ✅ `.env` file is in `.gitignore` (never committed to GitHub)
- ✅ Keys stored as environment variables on Render (encrypted)
- ✅ Backend code never exposes keys to frontend/users
- ✅ Only backend server can access the keys

❌ **Do NOT:**
- ❌ Commit `.env` file to GitHub
- ❌ Hardcode keys in code files
- ❌ Share keys publicly

---

## 🧪 Testing Your Setup

**Local:**
```bash
python3 app_fastapi.py
# Check logs for: "✅ Loaded N API key(s) from environment"
```

**Production:**
1. Check Render logs after deployment
2. Visit: https://elicitron-backend.onrender.com/api/health
3. Should return: `{"status": "healthy", ...}`

---

## 🆘 Troubleshooting

**Error: "No API keys found in environment variables"**
- **Local:** Check your `.env` file exists and has keys
- **Render:** Verify environment variables are set in dashboard

**Rate limit errors:**
- Add more API keys (increase `GOOGLE_API_KEY_N` count)
- System will automatically distribute load

**Keys not loading:**
- Ensure keys are named: `GOOGLE_API_KEY_1`, `GOOGLE_API_KEY_2` (with underscore and number)
- Check for typos in variable names
- Verify no extra spaces in key values

---

## 📝 Example Setup

**For 50 agents, you might need ~5-10 API keys:**

```bash
GOOGLE_API_KEY_1=AIzaSyKey1...
GOOGLE_API_KEY_2=AIzaSyKey2...
GOOGLE_API_KEY_3=AIzaSyKey3...
GOOGLE_API_KEY_4=AIzaSyKey4...
GOOGLE_API_KEY_5=AIzaSyKey5...
GOOGLE_API_KEY_6=AIzaSyKey6...
GOOGLE_API_KEY_7=AIzaSyKey7...
GOOGLE_API_KEY_8=AIzaSyKey8...
GOOGLE_API_KEY_9=AIzaSyKey9...
GOOGLE_API_KEY_10=AIzaSyKey10...
```

The system handles the rest automatically! 🚀
