from __future__ import annotations


# Keyword patterns for classification
SIMPLE_KEYWORDS = {
    "capital", "president", "when", "what is", "how many", "define",
    "convert", "calculate", "solve", "formula", "boiling point",
    "chemical", "list", "year", "who is", "what are", "how much",
    "abbreviation", "means", "stands for", "definition", "what does",
    "how long", "how far", "how heavy", "how tall", "temperature",
    "population", "distance", "height", "weight", "area",
}

COMPLEX_KEYWORDS = {
    "write", "explain", "design", "create", "function", "code",
    "python", "api", "story", "essay", "logic", "puzzle", "build",
    "develop", "algorithm", "schema", "architecture", "plan",
    "analyze", "compare", "debug", "optimize", "implement",
    "strategy", "compose", "generate", "how would", "why",
    "summarize", "review", "critique", "improve", "refactor",
    "discuss", "elaborate", "describe in detail", "teach me",
}


def _keyword_score(query: str, keywords: set) -> int:
    """Count keyword matches in query."""
    query_lower = query.lower()
    return sum(1 for keyword in keywords if keyword in query_lower)


def _estimate_response_tokens(query: str, route: str) -> int:
    """
    Estimate number of tokens in the response based on query type.
    
    Rough estimation:
    - Simple factual query: 50-100 tokens (short answer)
    - Complex query: 200-500 tokens (longer explanation)
    - Very complex (essay, code): 1000+ tokens
    """
    query_lower = query.lower()
    
    # Check for essay/story/code generation (very long responses)
    long_response_keywords = {
        "essay", "story", "write", "compose", "code", "function",
        "explain in detail", "how would", "design", "architecture"
    }
    if any(keyword in query_lower for keyword in long_response_keywords):
        return 300  # Long response expected
    
    # Simple queries usually get short answers
    if route == "Simple":
        return 50  # ~50 tokens for factual answer
    else:
        return 150  # Medium response for complex queries


def build_router():
    """Dummy function for compatibility."""
    return None


def classify_query(router, query: str) -> str:
    """
    Classify query into Simple or Complex using keyword matching.
    
    Simple: Factual recall, basic math, definitions, lookups
    Complex: Code, reasoning, analysis, creative writing, planning
    """
    simple_score = _keyword_score(query, SIMPLE_KEYWORDS)
    complex_score = _keyword_score(query, COMPLEX_KEYWORDS)
    
    # Debug logging
    print(f"📊 Query: '{query}'")
    print(f"   Simple score: {simple_score}, Complex score: {complex_score}")
    
    # If Simple has more matches, route to Simple
    if simple_score > complex_score and simple_score > 0:
        result = "Simple"
    # If Complex has more matches, route to Complex
    elif complex_score > simple_score and complex_score > 0:
        result = "Complex"
    # Tie-breaker: check for specific patterns
    elif simple_score == complex_score:
        query_lower = query.lower()
        if any(query_lower.startswith(prefix) for prefix in ["what is", "how many", "who is", "what are", "when", "where"]):
            result = "Simple"
        else:
            result = "Complex"
    else:
        result = "Complex"
    
    print(f"   ✅ Routed to: {result}\n")
    return result


def estimate_emissions(query: str, route: str, model: str) -> dict:
    """
    Estimate actual CO2 and water emissions based on:
    1. Query complexity (route)
    2. Expected response length (tokens)
    3. Model size (LLM vs SLM)
    
    Carbon/Water per 1000 tokens (token-normalized):
    - LLM: 0.15g CO2, 2.5ml water per 1000 tokens
    - SLM: 0.005g CO2, 0.08ml water per 1000 tokens
    """
    
    # Carbon and water per 1000 tokens (normalized)
    LLM_CARBON_PER_1K_TOKENS = 0.15   # grams
    LLM_WATER_PER_1K_TOKENS = 2.5     # ml
    SLM_CARBON_PER_1K_TOKENS = 0.005  # grams
    SLM_WATER_PER_1K_TOKENS = 0.08    # ml
    
    # Estimate response tokens
    response_tokens = _estimate_response_tokens(query, route)
    
    # Input tokens (query itself)
    input_tokens = len(query.split()) * 1.3  # Rough estimate: 1.3 tokens per word
    
    # Total tokens
    total_tokens = input_tokens + response_tokens
    
    if model == "SLM":
        carbon = (SLM_CARBON_PER_1K_TOKENS * total_tokens) / 1000
        water = (SLM_WATER_PER_1K_TOKENS * total_tokens) / 1000
    else:  # LLM
        carbon = (LLM_CARBON_PER_1K_TOKENS * total_tokens) / 1000
        water = (LLM_WATER_PER_1K_TOKENS * total_tokens) / 1000
    
    # Calculate savings: what we saved by NOT using LLM
    if model == "SLM":
        llm_carbon = (LLM_CARBON_PER_1K_TOKENS * total_tokens) / 1000
        llm_water = (LLM_WATER_PER_1K_TOKENS * total_tokens) / 1000
        carbon_saved = llm_carbon - carbon
        water_saved = llm_water - water
    else:
        # No savings if we used LLM (no alternative)
        carbon_saved = 0
        water_saved = 0
    
    print(f"🌍 Emissions Estimate:")
    print(f"   Input tokens: {input_tokens:.0f}")
    print(f"   Response tokens: {response_tokens}")
    print(f"   Total tokens: {total_tokens:.0f}")
    print(f"   {model} emissions: {carbon:.4f}g CO2, {water:.2f}ml water")
    print(f"   Savings: {carbon_saved:.4f}g CO2, {water_saved:.2f}ml water\n")
    
    return {
        "carbon_saved_g": round(carbon_saved, 4),
        "water_saved_ml": round(water_saved, 2),
        "emissions_carbon_g": round(carbon, 4),
        "emissions_water_ml": round(water, 2),
    }