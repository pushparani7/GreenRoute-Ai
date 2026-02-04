"""
Complexity Scorer - Analyzes query complexity to determine model routing
"""

from __future__ import annotations


class ComplexityScorer:
    """Score query complexity on multiple dimensions"""

    # Keywords indicating complex reasoning
    COMPLEX_KEYWORDS = {
        "explain", "analyze", "compare", "strategy", "design", "architecture",
        "how would", "why", "implement", "optimize", "debug", "solve",
        "summarize", "create", "write", "compose", "essay", "code",
        "algorithm", "pattern", "structure", "system"
    }

    # Keywords indicating simple queries
    SIMPLE_KEYWORDS = {
        "what is", "who is", "when", "where", "how many", "how much",
        "convert", "calculate", "define", "list", "what are",
        "capital", "president", "temperature", "distance"
    }

    @staticmethod
    def score_length(query: str) -> int:
        """Score based on query length"""
        words = len(query.split())

        if words < 5:
            return 1
        elif words < 10:
            return 2
        elif words < 20:
            return 3
        else:
            return 5

    @staticmethod
    def score_keywords(query: str) -> int:
        """Score based on keyword presence"""
        query_lower = query.lower()

        complex_matches = sum(1 for k in ComplexityScorer.COMPLEX_KEYWORDS
                             if k in query_lower)
        simple_matches = sum(1 for k in ComplexityScorer.SIMPLE_KEYWORDS
                             if k in query_lower)

        # Complex keywords are weighted higher
        keyword_score = (complex_matches * 3) - (simple_matches * 2)
        # Prevent large negative values (which would reduce total below 0)
        return max(keyword_score, 0)

    @staticmethod
    def score_punctuation(query: str) -> int:
        """Score based on punctuation patterns"""
        score = 0

        # Questions are often complex
        if "?" in query:
            score += 1

        # Multiple sentences suggest complexity
        if query.count(".") > 1:
            score += 2

        # Exclamations might indicate emphasis
        if "!" in query:
            score += 1

        # Colons suggest detailed explanations
        if ":" in query:
            score += 1

        return score

    @staticmethod
    def score_patterns(query: str) -> int:
        """Score based on common patterns"""
        query_lower = query.lower()
        score = 0

        # Code-related patterns
        code_patterns = ["function", "method", "class", "loop", "array", "variable"]
        score += sum(1 for p in code_patterns if p in query_lower) * 3

        # Analysis patterns
        analysis_patterns = ["trend", "pattern", "relationship", "correlation"]
        score += sum(1 for p in analysis_patterns if p in query_lower) * 2

        # Creative patterns
        creative_patterns = ["story", "poem", "essay", "creative", "imagine"]
        score += sum(1 for p in creative_patterns if p in query_lower) * 3

        return score

    @classmethod
    def compute_score(cls, query: str) -> dict:
        """
        Compute overall complexity score

        Returns:
            {
                "total_score": int,
                "length_score": int,
                "keyword_score": int,
                "punctuation_score": int,
                "pattern_score": int
            }
        """
        length_score = cls.score_length(query)
        keyword_score = cls.score_keywords(query)
        punctuation_score = cls.score_punctuation(query)
        pattern_score = cls.score_patterns(query)

        total_score = length_score + keyword_score + punctuation_score + pattern_score

        return {
            "total_score": max(0, total_score),  # Ensure non-negative
            "length_score": length_score,
            "keyword_score": keyword_score,
            "punctuation_score": punctuation_score,
            "pattern_score": pattern_score,
            "components": {
                "length": length_score,
                "keywords": keyword_score,
                "punctuation": punctuation_score,
                "patterns": pattern_score
            }
        }

    @classmethod
    def should_use_llm(cls, query: str, threshold: int = 12) -> bool:
        """
        Determine if query should use LLM (Mixtral)

        SLM (TinyLlama) for: < threshold
        LLM (Mixtral) for: >= threshold
        """
        score_data = cls.compute_score(query)
        return score_data["total_score"] >= threshold

    @staticmethod
    def get_routing_reason(score: int, threshold: int = 12) -> str:
        """
        Return a human readable routing reason given a numeric complexity score.
        This matches how ModelOrchestrator expects to call it.
        """
        if score >= threshold * 2:
            return f"High complexity (score={score}) — deep reasoning / multi-step required."
        if score >= threshold:
            return f"Complex (score={score}) — use LLM for better quality."
        if score >= int(threshold / 2):
            return f"Moderate complexity (score={score}) — SLM may work but LLM preferred for quality."
        return f"Simple (score={score}) — use SLM (fast, local)."
