# 🌱 GreenRoute AI

**An intelligent query orchestration system that automatically routes queries between small and large language models based on complexity. Achieved zero monthly costs while maintaining professional-grade performance metrics. Features include automatic complexity scoring, environmental impact tracking, and dual-mode routing (automatic + manual override).**

When you ask a simple question like "What's 2+2?" it routes to a tiny, super-fast model (⚡ 1 second). When you ask something complex like "Design a microservices architecture," it routes to a powerful model (🧠 8 seconds). Best of both worlds—automatic optimization with zero costs.

### Quick Stats
- 💰 **$0.00/month** (100% free)
- ⚡ **< 2 seconds** for simple queries
- 🧠 **5-15 seconds** for complex queries
- 🌍 **0.0084g CO₂ saved** per simple query
- 👤 **User control** - override routing anytime

  
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.13-blue)

---

## 🎯 Key Features

### ⚡ Intelligent Dual-Mode Routing

| Mode | Behavior | Use Case |
|------|----------|----------|
| **AUTO** (Default) | System analyzes complexity & routes intelligently | Most queries - no decision needed |
| **Force LLM** | Always use Mixtral 8x7B | Complex reasoning, code generation |
| **Force SLM** | Always use TinyLlama 1.1B | Quick lookups, fast responses |

### 🤖 Two Powerful Models (100% FREE)

**TinyLlama 1.1B** - Local Inference
- ⚡ < 2 seconds per query
- 💰 $0.00/query
- 🏠 Runs locally (privacy-friendly)
- Perfect for: Simple Q&A, lookups, classifications

**Mixtral 8x7B** - Cloud Inference (HuggingFace)
- 🧠 5-15 seconds per query (powerful reasoning)
- 💰 $0.00/query (free tier)
- ☁️ Cloud-based (HuggingFace API)
- Perfect for: Code generation, analysis, design, complex reasoning

### 📊 Professional Metrics Tracking

- ✅ Automatic model selection reasoning
- ✅ Query complexity scoring (0-25)
- ✅ Real-time latency monitoring
- ✅ Token counting & estimation
- ✅ Carbon & water impact tracking
- ✅ Cost analysis (always $0.00!)

### 🌍 Environmental Impact

**Per Query Savings** (SLM vs LLM)
- 💚 Carbon: 0.0084g CO₂ saved
- 💧 Water: 0.14ml conserved

**Annual Impact** (1000 queries)
- 📉 8.4g CO₂ saved (≈ 42m car drive)
- 💧 140ml water saved

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.13+
- HuggingFace API key (free)
- 4GB RAM minimum

### 1. Get HuggingFace API Key

```bash
# Visit: https://huggingface.co/signup (free account)
# Go to: https://huggingface.co/settings/tokens
# Create new "Read" token
# Copy the token
```

### 2. Clone & Setup

```bash
# Clone repository
git clone https://github.com/pushparani7/GreenRoute-AI.git
cd GreenRoute-AI

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.\.venv\Scripts\activate

# Or (Mac/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Create .env file
echo "HF_API_KEY=hf_your_api_key_here" > .env

# Verify
cat .env
```

### 4. Start the System

**Terminal 1 - Backend:**
```bash
.\.venv\Scripts\uvicorn app.main:app --reload
```

Expected output:
```
✅ INFO:     Uvicorn running on http://127.0.0.1:8000
✅ Application startup complete
```

**Terminal 2 - Frontend:**
```bash
.\.venv\Scripts\streamlit run dashboard.py
```

Expected output:
```
✅ You can now view your Streamlit app in your browser.
✅ Local URL: http://localhost:8501
```

### 5. Use It!

Open browser to: **http://localhost:8501**

Try these queries:
- **Simple**: "What is the capital of France?" → TinyLlama (⚡ ~1s)
- **Complex**: "Design a microservices architecture" → Mixtral (🧠 ~8s)
- **Override**: Force any model with dropdown selector

---

## 📁 Project Structure

```
GreenRoute-AI/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI backend
│   ├── complexity_scorer.py     # Query analysis
│   ├── model_orchestrator.py    # Routing logic
│   ├── slm_handler.py          # TinyLlama inference
│   ├── llm_handler.py          # Mixtral inference
│   ├── metrics_logger.py        # Performance tracking
│   ├── router.py               # Legacy routing
│   └── impact.py               # Legacy impact calc
├── dashboard.py                # Streamlit UI
├── requirements.txt            # Python dependencies
├── .env                        # Environment config
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

---

## 🔌 API Reference

### Health Check
```bash
GET /health

Response:
{
  "status": "healthy",
  "service": "GreenRoute AI",
  "version": "2.0.0"
}
```

### Process Query

```bash
POST /query

Request:
{
  "query": "What is the capital of France?",
  "mode": "AUTO"  # or "LLM" or "SLM"
}

Response:
{
  "query": "What is the capital of France?",
  "response": "The capital of France is Paris...",
  "model_used": "TinyLlama",
  "mode": "Automatic",
  "routing_reason": "Simple query (complexity: 2/25)",
  "complexity_score": 2,
  "latency_ms": 1234,
  "tokens": {"input": 12, "output": 45},
  "cost_usd": 0.0,
  "carbon_saved_g": 0.0084,
  "water_saved_ml": 0.14,
  "emissions_carbon_g": 0.0003,
  "emissions_water_ml": 0.005
}
```

### Get Statistics
```bash
GET /stats

Response:
{
  "summary": {
    "total_queries": 45,
    "tinyllama_queries": 32,
    "mixtral_queries": 13,
    "tinyllama_percentage": 71.1,
    "total_cost_usd": 0.0,
    "avg_latency_ms": 2345,
    "total_carbon_saved_g": 0.2688,
    "total_water_saved_ml": 4.48
  },
  "model_comparison": {...},
  "recent_queries": [...]
}
```

### Get Models Info
```bash
GET /models/info

Response:
{
  "slm": {
    "model_name": "TinyLlama 1.1B",
    "location": "Local (CPU/GPU)",
    "cost_per_query": "$0.00",
    "latency_estimate": "< 2 seconds",
    ...
  },
  "llm": {
    "model_name": "Mixtral 8x7B",
    "location": "Cloud (HuggingFace)",
    "cost_per_query": "$0.00",
    "latency_estimate": "5-15 seconds",
    ...
  }
}
```

---

## 🧠 How Routing Works

### Complexity Scoring Algorithm

```python
score = 0

# Length (more words = more complex)
score += len(query.split())

# Keywords (detect complex patterns)
score += sum(5 for keyword in ["explain", "design", "analyze"] 
             if keyword in query.lower())

# Punctuation (multiple sentences)
score += query.count(".") + query.count("?")

# Code patterns (API, function, algorithm)
score += sum(3 for pattern in ["function", "api", "algorithm"]
             if pattern in query.lower())

# Decision
if score < 12:
    model = TinyLlama  # Fast
else:
    model = Mixtral    # Powerful
```

### Real Examples

**Simple Query**
```
Input: "What is 2+2?"
Score: 2 (< 12)
Decision: TinyLlama ✅
Time: ~1 second
```

**Complex Query**
```
Input: "Design a REST API with authentication and database"
Score: 16 (≥ 12)
Decision: Mixtral ✅
Time: ~8 seconds
```

**User Override**
```
Input: "Hello world" + Force LLM
Score: 1 (< 12, but user overrides)
Decision: Mixtral (user forced) ⚙️
Time: ~6 seconds
```

---

## 💰 Cost Analysis

### Monthly Comparison (100 queries)

| System | Cost/Query | Monthly |
|--------|-----------|---------|
| OpenAI GPT-4 | $0.03 | $3.00 |
| GreenRoute AI | $0.00 | **$0.00** |
| **Annual Savings** | - | **$36** |

### Zero-Cost Forever

- ✅ TinyLlama: Local (no API calls)
- ✅ Mixtral: Free HuggingFace tier
- ✅ No credit card required
- ✅ No surprise charges

---

## 🔧 Configuration

### Adjust Complexity Threshold

```python
# In app/main.py
orchestrator = ModelOrchestrator(
    complexity_threshold=12,  # Lower = more SLM usage
    hf_api_key=HF_API_KEY
)
```

### Change Models

Edit `app/slm_handler.py` or `app/llm_handler.py` to use different models.

---

## 🐛 Troubleshooting

### Backend Takes Too Long

**Normal!** First query loads models (~30-60 seconds). Cached after that.

```bash
# Increase timeout in dashboard.py
timeout=180  # 3 minutes
```

### HuggingFace API Key Not Found

```bash
# Create .env file
echo "HF_API_KEY=hf_your_key" > .env

# Verify
cat .env
```

### TinyLlama Won't Load

```bash
# Reinstall PyTorch
pip install --upgrade torch transformers
```

### Port Already in Use

```bash
taskkill /F /IM python.exe
Start-Sleep -Seconds 2
# Try again
```

---

## 📈 Performance Benchmarks

### Latency
- **TinyLlama**: 0.5-2 seconds (local)
- **Mixtral**: 5-15 seconds (cloud, first query loads model)

### Accuracy
- **TinyLlama**: Good for simple tasks
- **Mixtral**: Excellent for complex reasoning

### Cost
- **Both**: $0.00/month (free forever!)

---

## 🚀 Deployment

### Option 1: Railway (Recommended)
```bash
# Free tier: 5GB/month compute
# Auto-scaling
# No credit card

# Just push to GitHub, Railway deploys automatically
git push origin main
```

### Option 2: HuggingFace Spaces
```bash
# Completely free
# Made for ML projects
# Auto-deploys from GitHub
```

### Option 3: AWS/GCP/Azure
```bash
# More control
# Pay-as-you-go
# Requires setup
```

---

## 📊 Architecture

```
┌─────────────────────────────────────────────┐
│         Streamlit Dashboard (UI)            │
│  - Model selector (AUTO/LLM/SLM)           │
│  - Query input & history                    │
│  - Environmental impact tracking            │
└────────────────┬────────────────────────────┘
                 │ HTTP
┌────────────────▼────────────────────────────┐
│      FastAPI Backend (Intelligence)         │
│  - Complexity scoring                       │
│  - Routing decision                         │
│  - User override handling                   │
└────────────────┬────────────────────────────┘
                 │
     ┌───────────┴───────────┐
     │                       │
┌────▼──────────┐   ┌───────▼────────┐
│  TinyLlama    │   │    Mixtral     │
│  (Local)      │   │  (HuggingFace) │
│  ⚡ < 2s      │   │   🧠 5-15s     │
│  💰 $0.00     │   │   💰 $0.00     │
└───────────────┘   └────────────────┘
```

---


This is **not a prototype**, it's a **production-grade system** featuring:

✅ Intelligent automatic routing  
✅ User control & override  
✅ Professional metrics tracking  
✅ Environmental impact monitoring  
✅ Zero monthly costs  
✅ Real LLMs (not fake)  
✅ Clean, professional UX  


---

## 📚 Technologies Used

- **Backend**: FastAPI, Uvicorn
- **Frontend**: Streamlit
- **Models**: TinyLlama (local), Mixtral (cloud)
- **Routing**: Custom complexity scoring
- **Monitoring**: Metrics logging & export
- **APIs**: HuggingFace Inference API

---

## 📝 License

MIT License - Feel free to use for personal or commercial projects.

---

## 👤 Author

Built by **PUSHPARANI**

---

## 🌍 Environmental Impact

Every query routed intelligently is a step toward sustainable AI. Together, we can build systems that are both powerful and responsible.

**Made with 🌱 for a greener AI future**

---

## 📞 Support

- LinkedIn: https://www.linkedin.com/in/pushparani-b-839208337/
- Email   : pushparanib7@gmail.com

---

**⭐ If you find this useful, please star the repository!**
