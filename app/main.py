from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from app.router import build_router, classify_query, estimate_emissions

app = FastAPI(title="GreenRoute AI")
router = build_router()


class RouteRequest(BaseModel):
    query: str


class RouteResponse(BaseModel):
    query: str
    route: str
    model: str
    carbon_saved_g: float
    water_saved_ml: float
    emissions_carbon_g: float
    emissions_water_ml: float


@app.post("/route", response_model=RouteResponse)
async def route_query(payload: RouteRequest) -> RouteResponse:
    """Route a query to appropriate model based on complexity."""
    route_name = classify_query(router, payload.query)
    
    # Simple queries go to SLM (Small Language Model) - saves carbon & water
    # Complex queries go to LLM (Large Language Model) - needed for reasoning
    if route_name == "Simple":
        model = "SLM"
    else:
        model = "LLM"
    
    # Calculate emissions based on actual query and response length
    emissions = estimate_emissions(payload.query, route_name, model)
    
    return RouteResponse(
        query=payload.query,
        route=route_name,
        model=model,
        carbon_saved_g=emissions["carbon_saved_g"],
        water_saved_ml=emissions["water_saved_ml"],
        emissions_carbon_g=emissions["emissions_carbon_g"],
        emissions_water_ml=emissions["emissions_water_ml"],
    )