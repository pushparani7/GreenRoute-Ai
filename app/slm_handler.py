"""
Small Language Model Handler - TinyLlama local inference
Fast, efficient, and completely free
"""

from __future__ import annotations
from typing import Optional
import torch


class SLMHandler:
    """
    Manages Small Language Model (TinyLlama)
    Runs locally for instant, free responses
    """
    
    MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    
    def __init__(self):
        """Initialize SLM handler"""
        self.model = None
        self.tokenizer = None
        self._initialized = False
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    def initialize(self) -> bool:
        """
        Lazy load the model (only when needed)
        First run downloads ~2GB model file
        
        Returns:
            True if initialized successfully
        """
        if self._initialized:
            return True
        
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            
            print(f"📥 Loading TinyLlama (device: {self.device})")
            print(f"   Model: {self.MODEL_NAME}")
            print("   ⏳ This takes ~30-60 seconds on first run...")
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.MODEL_NAME)
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.MODEL_NAME,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None
            )
            
            if self.device == "cpu":
                self.model = self.model.to(self.device)
            
            self._initialized = True
            print("✅ TinyLlama loaded successfully")
            return True
        
        except Exception as e:
            print(f"❌ Error loading TinyLlama: {e}")
            return False
    
    def generate_response(self, prompt: str, max_tokens: int = 150) -> str:
        """
        Generate response using TinyLlama
        
        Args:
            prompt: User query/prompt
            max_tokens: Maximum tokens to generate
        
        Returns:
            Generated response text
        """
        if not self._initialized:
            if not self.initialize():
                return "Error: Could not initialize TinyLlama"
        
        try:
            # Format prompt as chat
            formatted_prompt = f"User: {prompt}\nAssistant:"
            
            # Tokenize
            inputs = self.tokenizer(
                formatted_prompt,
                return_tensors="pt",
                truncation=True,
                max_length=512
            ).to(self.device)
            
            # Generate
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    temperature=0.7,
                    top_p=0.95,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                )
            
            # Decode
            response = self.tokenizer.decode(
                outputs[0][inputs["input_ids"].shape[1]:],
                skip_special_tokens=True
            )
            
            return response.strip()
        
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text
        
        Args:
            text: Input text
        
        Returns:
            Number of tokens
        """
        if not self._initialized:
            self.initialize()
        
        try:
            tokens = self.tokenizer.encode(text)
            return len(tokens)
        except:
            # Rough estimate: ~4 characters per token
            return int(len(text) / 4)
    
    def get_model_info(self) -> dict:
        """Get information about the model"""
        return {
            "model_name": "TinyLlama 1.1B",
            "model_type": "Small Language Model (SLM) - Local",
            "location": "Local (CPU/GPU)",
            "parameters": "1.1 Billion",
            "cost_per_query": "$0.00 (FREE)",
            "latency_estimate": "0.5-2 seconds",
            "memory_required": "2-4 GB",
            "strengths": [
                "Instant (runs locally)",
                "Completely FREE",
                "Offline capable",
                "Privacy-friendly",
                "Fast responses"
            ],
            "weaknesses": [
                "Limited reasoning ability",
                "Smaller knowledge base",
                "Can hallucinate on complex tasks"
            ],
            "best_for": [
                "Simple Q&A",
                "Classifications",
                "Summaries",
                "Knowledge lookups",
                "First-pass filtering"
            ],
            "hardware": {
                "minimum_ram": "4GB",
                "gpu_optional": "But recommended",
                "download_size": "~2GB"
            }
        }