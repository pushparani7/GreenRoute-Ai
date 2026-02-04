"""
Model Orchestrator - Intelligent routing between SLM and Mixtral
Executes the routed model and RETURNS THE ANSWER
"""

from __future__ import annotations
import time
from app.complexity_scorer import ComplexityScorer
from app.slm_handler import SLMHandler
from app.llm_handler import LLMHandler
from app.metrics_logger import MetricsLogger


class ModelOrchestrator:
    """
    Intelligent query orchestration system

    Modes:
    - AUTO : system decides SLM vs LLM
    - SLM  : force TinyLlama
    - LLM  : force Mixtral
    """

    def __init__(self, complexity_threshold: int = 12, hf_api_key: str = None):
        self.complexity_threshold = complexity_threshold

        self.slm = SLMHandler()          # TinyLlama (local)
        self.llm = LLMHandler(hf_api_key=hf_api_key)  # Mixtral (HF)

        self.metrics = MetricsLogger()

    def process_query(self, query: str, mode: str = "AUTO") -> dict:
        start_time = time.time()

        # 1️⃣ Complexity scoring
        complexity_data = ComplexityScorer.compute_score(query)
        complexity_score = complexity_data["total_score"]

        # 2️⃣ Routing + EXECUTION (this is the critical part)
        if mode == "LLM":
            response, tokens, cost = self._process_with_llm(query)
            model_used = "Mixtral"
            routing_reason = "User forced LLM"
            routing_mode = "User Override"
            carbon_saved = 0.0
            water_saved = 0.0

        elif mode == "SLM":
            response, tokens, cost = self._process_with_slm(query)
            model_used = "TinyLlama"
            routing_reason = "User forced SLM"
            routing_mode = "User Override"
            carbon_saved = self._calculate_carbon_saved(tokens["output"])
            water_saved = self._calculate_water_saved(tokens["output"])

        else:  # AUTO
            if complexity_score >= self.complexity_threshold:
                response, tokens, cost = self._process_with_llm(query)
                model_used = "Mixtral"
                carbon_saved = 0.0
                water_saved = 0.0
            else:
                response, tokens, cost = self._process_with_slm(query)
                model_used = "TinyLlama"
                carbon_saved = self._calculate_carbon_saved(tokens["output"])
                water_saved = self._calculate_water_saved(tokens["output"])

            routing_reason = ComplexityScorer.get_routing_reason(complexity_score)
            routing_mode = "Automatic"

        # 🛡️ Fail-safe: never return empty answer
        if not response or not response.strip():
            response = "⚠️ Model executed but returned an empty response."

        latency = time.time() - start_time

        # 3️⃣ Log metrics
        self.metrics.log_query(
            query=query,
            complexity_score=complexity_score,
            model_used=model_used,
            latency=latency,
            input_tokens=tokens["input"],
            output_tokens=tokens["output"],
            cost=cost,
            response=response,
            carbon_saved=carbon_saved,
            water_saved=water_saved
        )

        # 4️⃣ Final response (API + UI SAFE)
        return {
            "query": query,
            "response": response,  # ✅ THIS IS THE ANSWER
            "model_used": model_used,
            "mode": routing_mode,
            "routing_reason": routing_reason,
            "complexity_score": complexity_score,
            "complexity_breakdown": complexity_data["components"],
            "latency_ms": round(latency * 1000, 2),
            "tokens": tokens,
            "cost_usd": round(cost, 6),
            "carbon_saved_g": round(carbon_saved, 4),
            "water_saved_ml": round(water_saved, 2),
            "emissions_carbon_g": round(
                self._calculate_emissions_carbon(tokens["output"], model_used), 4
            ),
            "emissions_water_ml": round(
                self._calculate_emissions_water(tokens["output"], model_used), 2
            )
        }

    # ---------------- INTERNAL EXECUTION ---------------- #

    def _process_with_slm(self, query: str) -> tuple:
        response = self.slm.generate_response(query, max_tokens=150)
        input_tokens = self.slm.count_tokens(query)
        output_tokens = self.slm.count_tokens(response)
        return response, {"input": input_tokens, "output": output_tokens}, 0.0

    def _process_with_llm(self, query: str) -> tuple:
        response = self.llm.generate_response(query, max_tokens=500)
        input_tokens = self.llm.count_tokens(query)
        output_tokens = self.llm.count_tokens(response)
        cost = self.llm.estimate_cost(input_tokens, output_tokens)
        return response, {"input": input_tokens, "output": output_tokens}, cost

    # ---------------- METRICS ---------------- #

    @staticmethod
    def _calculate_carbon_saved(output_tokens: int) -> float:
        return (output_tokens / 1000) * (0.15 - 0.005)

    @staticmethod
    def _calculate_water_saved(output_tokens: int) -> float:
        return (output_tokens / 1000) * (2.5 - 0.08)

    @staticmethod
    def _calculate_emissions_carbon(output_tokens: int, model_used: str) -> float:
        return (output_tokens / 1000) * (0.15 if model_used == "Mixtral" else 0.005)

    @staticmethod
    def _calculate_emissions_water(output_tokens: int, model_used: str) -> float:
        return (output_tokens / 1000) * (2.5 if model_used == "Mixtral" else 0.08)

    def get_orchestrator_stats(self) -> dict:
        return {
            "summary": self.metrics.get_summary(),
            "model_comparison": self.metrics.get_model_comparison(),
            "recent_queries": self.metrics.get_recent_metrics(limit=5)
        }
