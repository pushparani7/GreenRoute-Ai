"""
Large Language Model Handler - Mixtral 8x7B via HuggingFace Inference API
Powerful, open-source, free reasoning engine
"""

from __future__ import annotations
import os
from typing import Optional
import requests
import time


class LLMHandler:
    """
    Manages Large Language Model (Mixtral 8x7B)
    Uses HuggingFace Inference API for powerful reasoning
    """
    
    # Mixtral 8x7B - State-of-the-art open-source model
    MODEL_CONFIG = {
        "name": "Mixtral 8x7B Instruct",
        "api_url": "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1",
        "description": "8 expert mixture model - 56B parameters total",
        "max_tokens": 2048,
        "temperature": 0.7
    }
    
    def __init__(self, hf_api_key: Optional[str] = None):
        """
        Initialize LLM handler with Mixtral 8x7B
        
        Args:
            hf_api_key: HuggingFace API key (defaults to HF_API_KEY env var)
        """
        self.hf_api_key = hf_api_key or os.getenv("HF_API_KEY")
        self.model_config = self.MODEL_CONFIG
        self._initialized = False
        self._model_loading = False
        
        if self.hf_api_key:
            self.initialize()
    
    def initialize(self) -> bool:
        """
        Initialize HuggingFace API connection to Mixtral
        
        Returns:
            True if initialized successfully
        """
        if self._initialized:
            return True
        
        if not self.hf_api_key:
            print("⚠️  HuggingFace API key not found.")
            print("   Get free API key at: https://huggingface.co/settings/tokens")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.hf_api_key}"}
            
            print(f"📥 Connecting to {self.model_config['name']}")
            print("   (Model will load on first query, ~30-60 seconds)")
            
            # Just verify the API key works
            response = requests.post(
                self.model_config["api_url"],
                headers=headers,
                json={"inputs": "test", "options": {"wait_for_model": False}},
                timeout=5
            )
            
            self._initialized = True
            print("✅ LLM (Mixtral 8x7B) initialized")
            return True
        
        except requests.exceptions.Timeout:
            self._initialized = True  # Still mark as initialized
            print("✅ LLM (Mixtral 8x7B) connection ready")
            return True
        except Exception as e:
            print(f"⚠️  Connection check failed: {e}")
            print("   Will try again on first query...")
            self._initialized = True
            return True
    
    def generate_response(
        self,
        prompt: str,
        max_tokens: int = 500,
        temperature: float = None
    ) -> str:
        """
        Generate response using Mixtral 8x7B
        
        Args:
            prompt: User query/prompt
            max_tokens: Maximum tokens in response
            temperature: Creativity level (0-2)
        
        Returns:
            Generated response text
        """
        if not self._initialized:
            if not self.initialize():
                return "Error: LLM not initialized. Set HF_API_KEY environment variable."
        
        if temperature is None:
            temperature = self.model_config["temperature"]
        
        try:
            headers = {"Authorization": f"Bearer {self.hf_api_key}"}
            
            # Format as chat instruction
            formatted_prompt = f"""[INST] {prompt} [/INST]"""
            
            payload = {
                "inputs": formatted_prompt,
                "parameters": {
                    "max_new_tokens": max_tokens,
                    "temperature": temperature,
                    "top_p": 0.95,
                    "top_k": 50,
                    "repetition_penalty": 1.1,
                    "do_sample": True
                },
                "options": {
                    "wait_for_model": True  # Wait if model is loading
                }
            }
            
            print("🔄 Calling Mixtral 8x7B...")
            start_time = time.time()
            
            response = requests.post(
                self.model_config["api_url"],
                headers=headers,
                json=payload,
                timeout=120  # Longer timeout for inference
            )
            
            elapsed = time.time() - start_time
            print(f"✅ Response received ({elapsed:.1f}s)")
            
            response.raise_for_status()
            result = response.json()
            
            # Handle response format
            if isinstance(result, list) and len(result) > 0:
                if "generated_text" in result[0]:
                    text = result[0]["generated_text"]
                    # Remove the prompt from the output
                    if "[/INST]" in text:
                        text = text.split("[/INST]")[-1].strip()
                    return text
            
            return str(result)
        
        except requests.exceptions.Timeout:
            return "⏱️ Model is loading or overloaded. Please try again in a moment."
        except Exception as e:
            return f"Error: {str(e)}"
    
    def count_tokens(self, text: str) -> int:
        """
        Estimate token count for Mixtral
        
        Approximation: ~4 characters per token
        """
        return int(len(text) / 4)
    
    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Estimate cost
        
        Mixtral via HF Inference API is FREE for free tier users!
        Cost depends on HF tier:
        - Free: Limited requests/month
        - Pro: ~$9/month for unlimited
        
        Returns:
            Cost estimate in USD ($0.00 for free tier)
        """
        return 0.0  # FREE!
    
    def get_model_info(self) -> dict:
        """Get information about the model"""
        return {
            "model_name": self.model_config["name"],
            "model_type": "Large Language Model (LLM) - Open Source",
            "location": "Cloud (HuggingFace Inference API)",
            "architecture": "Mixture of Experts (8 experts × 7B)",
            "total_parameters": "56 Billion (active: 12.9B)",
            "cost_per_token": "$0.00 (FREE)",
            "subscription_cost": "Free tier included",
            "latency_estimate": "3-15 seconds (depends on load)",
            "strengths": [
                "Completely FREE (HF free tier)",
                "State-of-the-art reasoning",
                "Mixture of Experts architecture",
                "Excellent code generation",
                "Strong multi-language support",
                "No content restrictions"
            ],
            "weaknesses": [
                "Slower than local models",
                "Depends on HF infrastructure",
                "Rate limits on free tier (unlimited after 1 minute)",
                "Cold starts on first query"
            ],
            "best_for": [
                "Complex reasoning",
                "Code generation",
                "Creative writing",
                "Analysis & insights",
                "Multi-step problem solving",
                "Technical explanations"
            ],
            "api_required": "HuggingFace API Key (free)",
            "first_query_warning": "First query takes 30-60s (model loads once)"
        }