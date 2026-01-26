# GreenRoute AI 🌱

Carbon-aware model router using **FastAPI + Streamlit**. Intelligently routes simple queries to Small Language Models (SLM) and complex queries to Large Language Models (LLM) to minimize environmental impact.

## 🌍 Features

- ✅ **Smart Query Routing** - Classifies queries as Simple or Complex
- ✅ **Real-time Emissions Tracking** - Carbon & water usage per query
- ✅ **Token-based Calculation** - Accurate impact based on query complexity
- ✅ **Interactive Dashboard** - Beautiful Streamlit UI with metrics
- ✅ **FastAPI Backend** - RESTful API with automatic docs
- ✅ **Zero API Keys** - Uses local HuggingFace embeddings

## 📊 How It Works
`
User Query → Router Classification → Model Selection → Emissions Calculate
    ↓              ↓                      ↓                    ↓
"What is        Simple? or          SLM or LLM         0.0084g CO₂
the capital?"   Complex?            (routing)          0.14ml water
`

### Routing Logic

| Query Type | Example | Route | Model | Emissions |
|-----------|---------|-------|-------|-----------|
| **Simple** | "What is the capital of France?" | Simple | SLM | 0.0003g CO₂ |
| **Complex** | "Write a Python sorting function" | Complex | LLM | 0.0471g CO₂ |

### Savings Example

- 1 simple query routed to SLM instead of LLM: **0.0084g CO₂ saved**
- 1000 simple queries: **8.4g CO₂ saved** (equivalent to ~42m car drive)

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Git

### Installation
`ash
# Clone the repo
git clone https://github.com/pushparani7/GreenRoute-Ai.git
cd GreenRoute_ai

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
`

### Run the Application

**Option 1: Start both services together**
`ash
.\start.ps1
`

**Option 2: Start separately**

Terminal 1 - Backend:
`ash
.\.venv\Scripts\uvicorn app.main:app --reload
`
Backend: http://localhost:8000
API Docs: http://localhost:8000/docs

Terminal 2 - Frontend:
`ash
.\.venv\Scripts\streamlit run dashboard.py
`
Frontend: http://localhost:8501

## 📁 Project Structure
`
GreenRoute-Ai/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app & /route endpoint
│   ├── router.py         # Query classification & emissions calculation
│   └── impact.py         # Legacy impact functions
├── dashboard.py          # Streamlit dashboard
├── requirements.txt      # Dependencies
├── start.ps1            # Start script
├── .gitignore
└── README.md
`

## 🔌 API Documentation

### POST /route

**Request:**
`json
{
  "query": "What is the capital of France?"
}
`

**Response:**
`json
{
  "query": "What is the capital of France?",
  "route": "Simple",
  "model": "SLM",
  "carbon_saved_g": 0.0084,
  "water_saved_ml": 0.14,
  "emissions_carbon_g": 0.0003,
  "emissions_water_ml": 0.005
}
`

### Query Classification

**Simple Queries** (route to SLM):
- Factual recalls: "What is the capital of France?"
- Math: "Convert 10 miles to kilometers"
- Definitions: "What is photosynthesis?"

**Complex Queries** (route to LLM):
- Code generation: "Write a Python function to sort a list"
- Analysis: "Explain how machine learning works"
- Creative: "Write a short story about AI"

## 📊 Emissions Benchmarks (2026)

Per query execution:

| Model | CO₂ Emissions | Water Usage |
|-------|---------------|-------------|
| **LLM** | 0.15g per 1000 tokens | 2.5ml per 1000 tokens |
| **SLM** | 0.005g per 1000 tokens | 0.08ml per 1000 tokens |

**Estimated Response Lengths:**
- Simple query: ~50 tokens
- Complex query: ~300 tokens

## 🎯 Environmental Impact

### Real-World Equivalent

- **0.0084g CO₂ saved per simple query** = 1 meter of car driving
- **1,000 queries** = 8.4g CO₂ = ~42 meters car driving
- **10,000 queries** = 84g CO₂ = ~420 meters car driving

### Monthly Impact (100 queries)

Using SLM for simple queries instead of LLM:
- **Carbon saved:** 0.84g CO₂
- **Water saved:** 1.4ml
- **Equivalent to:** 4.2 meters of car driving avoided

## 🔧 Technologies Used

- **Backend:** FastAPI, Uvicorn
- **Frontend:** Streamlit, Plotly
- **Routing:** semantic-router, HuggingFace Transformers
- **Embeddings:** sentence-transformers/all-MiniLM-L6-v2

## 📈 Future Enhancements

- [ ] Multi-language query support
- [ ] Custom embedding models
- [ ] Real-time energy price integration
- [ ] Advanced analytics & reporting
- [ ] Model fine-tuning capabilities
- [ ] Batch query processing
- [ ] Database for historical tracking
- [ ] Dockerization

## 🤝 Contributing

Contributions welcome! Feel free to:
1. Fork the repository
2. Create a feature branch (git checkout -b feature/amazing-feature)
3. Commit changes (git commit -m 'Add amazing feature')
4. Push to branch (git push origin feature/amazing-feature)
5. Open a Pull Request

## 📜 License

MIT License - feel free to use this project for personal or commercial purposes

## 👤 Author

Built by **pushparani7** with ❤️

## 🌍 Impact

Every query routed intelligently is a step towards sustainable AI. Together, we can build systems that are both powerful and responsible.

---

**Made with 🌱 for a greener AI future**
