# GreenRoute AI

Carbon-aware model router using FastAPI + Streamlit.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
```

## Run

```powershell
.\start.ps1
```

## Manual Run

```powershell
.\.venv\Scripts\uvicorn app.main:app --reload
```

```powershell
.\.venv\Scripts\streamlit run dashboard.py
```

## Notes

- The router uses `semantic-router` with an OpenAI encoder. Set your `OPENAI_API_KEY` in the environment before running.
