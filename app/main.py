from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel
from app.model_orchestrator import ModelOrchestrator
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env if present (safe local development)
load_dotenv()

app = FastAPI(
    title="GreenRoute AI",
    description="""
    Intelligent Query Orchestration System
    
    Automatically routes queries between:
    - **TinyLlama 1.1B** (Local, instant, free) for simple tasks
    - **Mixtral 8x7B** (Cloud, powerful, free) for complex reasoning
    
    Architecture:
    - Complexity Scoring: Analyzes query difficulty
    - Smart Routing: Routes based on computational needs
    - Metrics Tracking: Monitors latency, cost, carbon impact
    - Environmental Monitoring: Tracks carbon & water savings
    """,
    version="2.0.0"
)

# Initialize orchestrator with open-source models
HF_API_KEY = os.getenv("HF_API_KEY")
orchestrator = ModelOrchestrator(
    complexity_threshold=12,  # Lower threshold = more SLM usage
    hf_api_key=HF_API_KEY
)

@app.on_event("startup")
async def startup_prewarm_models():
    """Pre-warm local SLM and remote LLM on startup in background threads.

    This avoids cold-start latency during the first user request. Runs
    initialization in threads so the FastAPI event loop is not blocked.
    """
    async def _prewarm():
        slm_ok = await asyncio.to_thread(orchestrator.slm.initialize)
        llm_ok = await asyncio.to_thread(orchestrator.llm.initialize)
        print(f"🔁 Startup pre-warm complete: SLM initialized={slm_ok}, LLM initialized={llm_ok}")

    # Schedule pre-warm asynchronously and don't await to keep startup fast
    asyncio.create_task(_prewarm())

class QueryRequest(BaseModel):
    query: str
    mode: str = "AUTO"


class QueryResponse(BaseModel):
    query: str
    response: str
    model_used: str
    mode: str
    complexity_score: int
    routing_reason: str
    latency_ms: float
    tokens: dict
    cost_usd: float
    carbon_saved_g: float
    water_saved_ml: float
    emissions_carbon_g: float
    emissions_water_ml: float


class StatsResponse(BaseModel):
    summary: dict
    model_comparison: dict
    recent_queries: list


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "GreenRoute AI",
        "version": "2.0.0"
    }


@app.post("/query", response_model=QueryResponse)
async def process_query(payload: QueryRequest) -> QueryResponse:
    """
    Process a query with automatic model selection
    
    The orchestrator automatically:
    1. Analyzes query complexity
    2. Decides between SLM and LLM
    3. Generates response
    4. Calculates environmental impact
    5. Logs metrics
    """
    # Run the blocking orchestration in a separate thread to avoid
    # blocking the FastAPI event loop (SLM/LLM calls are synchronous).
    result = await asyncio.to_thread(orchestrator.process_query, payload.query, payload.mode)
    
    return QueryResponse(
        query=result["query"],
        response=result["response"],
        model_used=result["model_used"],
        mode=result.get("mode", "Automatic"),
        complexity_score=result["complexity_score"],
        routing_reason=result.get("routing_reason", ""),
        latency_ms=result["latency_ms"],
        tokens=result["tokens"],
        cost_usd=result["cost_usd"],
        carbon_saved_g=result["carbon_saved_g"],
        water_saved_ml=result["water_saved_ml"]
        ,emissions_carbon_g=result["emissions_carbon_g"],
        emissions_water_ml=result["emissions_water_ml"]
    )


@app.get("/stats", response_model=StatsResponse)
async def get_statistics() -> StatsResponse:
    """Get system statistics and metrics"""
    stats = orchestrator.get_orchestrator_stats()
    
    return StatsResponse(
        summary=stats["summary"],
        model_comparison=stats["model_comparison"],
        recent_queries=stats["recent_queries"]
    )


@app.get("/metrics/export")
async def export_metrics():
    """Export metrics to file"""
    filepath = "greenroute_metrics.json"
    if orchestrator.metrics.export_metrics(filepath):
        return {
            "status": "success",
            "filepath": filepath,
            "message": "Metrics exported successfully"
        }
    else:
        return {
            "status": "error",
            "message": "Failed to export metrics"
        }


@app.get("/models/info")
async def get_models_info():
    """Get information about available models"""
    return {
        "slm": orchestrator.slm.get_model_info(),
        "llm": orchestrator.llm.get_model_info(),
        "routing_threshold": orchestrator.complexity_threshold
    }


@app.post("/config/threshold")
async def set_complexity_threshold(threshold: int):
    """Update complexity threshold for routing"""
    if 0 <= threshold <= 100:
        orchestrator.complexity_threshold = threshold
        return {
            "status": "success",
            "new_threshold": threshold
        }
    else:
        return {
            "status": "error",
            "message": "Threshold must be between 0 and 100"
        }