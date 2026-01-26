from __future__ import annotations

# These constants are DEPRECATED - use estimate_emissions() in router.py instead
# Keeping for reference only

LLM_CARBON_G = 0.3
LLM_WATER_ML = 5.0
SLM_CARBON_G = 0.01
SLM_WATER_ML = 0.1


def calculate_savings(slm_calls: int) -> dict[str, float]:
    """
    DEPRECATED: This uses fixed values and doesn't account for query complexity.
    Use estimate_emissions() from router.py instead.
    
    Legacy function kept for backward compatibility.
    """
    carbon_saved = (LLM_CARBON_G - SLM_CARBON_G) * slm_calls
    water_saved = (LLM_WATER_ML - SLM_WATER_ML) * slm_calls
    return {"carbon_saved_g": carbon_saved, "water_saved_ml": water_saved}