"""
Metrics Logger - Tracks system performance and costs
"""

from __future__ import annotations
from datetime import datetime
from typing import Optional
import json


class MetricsLogger:
    """Logs and tracks metrics for monitoring and analysis"""
    
    def __init__(self):
        """Initialize metrics logger"""
        self.metrics = []
    
    def log_query(
        self,
        query: str,
        complexity_score: int,
        model_used: str,
        latency: float,
        input_tokens: int,
        output_tokens: int,
        cost: float,
        response: str,
        carbon_saved: float = 0.0,
        water_saved: float = 0.0
    ) -> dict:
        """
        Log a query execution
        
        Args:
            query: Original query
            complexity_score: Computed complexity score
            model_used: "TinyLlama" or "Mixtral"
            latency: Response time in seconds
            input_tokens: Tokens in input
            output_tokens: Tokens in output
            cost: API cost in USD
            response: Generated response
            carbon_saved: CO2 saved in grams
            water_saved: Water saved in ml
        
        Returns:
            Metric entry as dictionary
        """
        metric = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "complexity_score": complexity_score,
            "model_used": model_used,
            "latency_ms": round(latency * 1000, 2),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "cost_usd": round(cost, 6),
            "response_preview": response[:100] if response else "",
            "carbon_saved_g": round(carbon_saved, 4),
            "water_saved_ml": round(water_saved, 2)
        }
        
        self.metrics.append(metric)
        return metric
    
    def get_summary(self) -> dict:
        """
        Get summary statistics
        
        Returns:
            Summary dictionary with aggregated metrics
        """
        if not self.metrics:
            return {
                "total_queries": 0,
                "tinyllama_queries": 0,
                "mixtral_queries": 0,
                "total_cost": 0.0,
                "total_latency": 0.0,
                "avg_latency": 0.0,
                "total_tokens": 0,
                "total_carbon_saved": 0.0,
                "total_water_saved": 0.0
            }
        
        tinyllama_count = sum(1 for m in self.metrics if m["model_used"] == "TinyLlama")
        mixtral_count = sum(1 for m in self.metrics if m["model_used"] == "Mixtral")
        total_cost = sum(m["cost_usd"] for m in self.metrics)
        total_latency = sum(m["latency_ms"] for m in self.metrics)
        total_tokens = sum(m["total_tokens"] for m in self.metrics)
        total_carbon_saved = sum(m["carbon_saved_g"] for m in self.metrics)
        total_water_saved = sum(m["water_saved_ml"] for m in self.metrics)
        
        return {
            "total_queries": len(self.metrics),
            "tinyllama_queries": tinyllama_count,
            "mixtral_queries": mixtral_count,
            "tinyllama_percentage": round((tinyllama_count / len(self.metrics) * 100), 1) if self.metrics else 0,
            "total_cost_usd": round(total_cost, 4),
            "total_latency_ms": round(total_latency, 2),
            "avg_latency_ms": round(total_latency / len(self.metrics), 2) if self.metrics else 0,
            "total_tokens": total_tokens,
            "avg_tokens_per_query": round(total_tokens / len(self.metrics), 1) if self.metrics else 0,
            "total_carbon_saved_g": round(total_carbon_saved, 4),
            "total_water_saved_ml": round(total_water_saved, 2),
            "cost_per_query": round(total_cost / len(self.metrics), 6) if self.metrics else 0
        }
    
    def get_model_comparison(self) -> dict:
        """
        Compare TinyLlama vs Mixtral metrics
        
        Returns:
            Comparison dictionary
        """
        tinyllama_metrics = [m for m in self.metrics if m["model_used"] == "TinyLlama"]
        mixtral_metrics = [m for m in self.metrics if m["model_used"] == "Mixtral"]
        
        tinyllama_summary = self._summarize_metrics(tinyllama_metrics)
        mixtral_summary = self._summarize_metrics(mixtral_metrics)
        
        return {
            "tinyllama": tinyllama_summary,
            "mixtral": mixtral_summary,
            "speed_difference": mixtral_summary["avg_latency"] - tinyllama_summary["avg_latency"],
            "tinyllama_faster_by": round((1 - tinyllama_summary["avg_latency"] / max(mixtral_summary["avg_latency"], 0.00001)) * 100, 1)
        }
    
    @staticmethod
    def _summarize_metrics(metrics: list) -> dict:
        """Summarize a list of metrics"""
        if not metrics:
            return {
                "count": 0,
                "avg_latency": 0,
                "avg_cost": 0,
                "avg_tokens": 0
            }
        
        return {
            "count": len(metrics),
            "avg_latency": round(sum(m["latency_ms"] for m in metrics) / len(metrics), 2),
            "avg_cost": round(sum(m["cost_usd"] for m in metrics) / len(metrics), 6),
            "avg_tokens": round(sum(m["total_tokens"] for m in metrics) / len(metrics), 1),
            "total_cost": round(sum(m["cost_usd"] for m in metrics), 4)
        }
    
    def get_recent_metrics(self, limit: int = 10) -> list:
        """Get recent metrics"""
        return self.metrics[-limit:]
    
    def export_metrics(self, filepath: str) -> bool:
        """
        Export metrics to JSON file
        
        Args:
            filepath: Path to save metrics
        
        Returns:
            True if successful
        """
        try:
            with open(filepath, 'w') as f:
                json.dump({
                    "metrics": self.metrics,
                    "summary": self.get_summary(),
                    "comparison": self.get_model_comparison()
                }, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting metrics: {e}")
            return False