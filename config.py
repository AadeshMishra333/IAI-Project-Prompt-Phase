"""
Configuration for Prompt Intent Classifier

This module defines the classification rubric, labels, and scoring thresholds
for the multi-label prompt intent classification system.
"""

# Classification dimensions and their definitions
DIMENSIONS = {
    "coding": {
        "label": "Coding",
        "description": "Code generation, debugging, algorithms, implementation, syntax",
        "examples": [
            "write a python function to sort a list",
            "debug this recursive function",
            "how do I implement binary search?",
            "fix the syntax error in my code"
        ]
    },
    "reasoning": {
        "label": "Reasoning",
        "description": "Logical deduction, analysis, step-by-step thinking, problem decomposition",
        "examples": [
            "explain how this algorithm works step by step",
            "break down this complex problem",
            "what is the logical flow here?",
            "analyze the pros and cons"
        ]
    },
    "plain_language_conversion": {
        "label": "Plain Language/Conversion",
        "description": "Rewrite, simplify, translate, paraphrase, clarification",
        "examples": [
            "simplify this sentence for a 5-year-old",
            "translate this to French",
            "rewrite this more concisely",
            "explain this in simpler terms"
        ]
    },
    "math": {
        "label": "Math",
        "description": "Calculation, proof, algebra, probability, equations, statistics",
        "examples": [
            "solve this quadratic equation",
            "calculate the probability of rolling two dice",
            "prove this mathematical theorem",
            "what is 25% of 400?"
        ]
    },
    "factual": {
        "label": "Factual",
        "description": "Information retrieval, explanation of real-world facts, research",
        "examples": [
            "what is the capital of France?",
            "explain photosynthesis",
            "how does gravity work?",
            "tell me about the history of the internet"
        ]
    },
    "creative_tone": {
        "label": "Creative/Tone",
        "description": "Jokes, stories, poetry, style adaptation, marketing copy, humor",
        "examples": [
            "tell me a funny joke",
            "write a haiku about programming",
            "compose a marketing pitch for this product",
            "write a creative story about a robot"
        ]
    }
}

# Ordered list of dimension keys for consistent ordering
DIMENSION_KEYS = [
    "coding",
    "reasoning",
    "plain_language_conversion",
    "math",
    "factual",
    "creative_tone"
]

# Score interpretation thresholds (0-1 scale)
SCORE_THRESHOLDS = {
    "high": 0.7,
    "medium_high": 0.5,
    "medium": 0.4,
    "medium_low": 0.3,
    "low": 0.0
}

# Helper function to interpret scores
def interpret_score(score):
    """Convert numeric score to text label."""
    if score >= SCORE_THRESHOLDS["high"]:
        return "High"
    elif score >= SCORE_THRESHOLDS["medium"]:
        return "Medium"
    else:
        return "Low"

def get_color_for_score(score):
    """Return color for visualization based on score."""
    if score >= SCORE_THRESHOLDS["high"]:
        return "#4CAF50"  # Green
    elif score >= SCORE_THRESHOLDS["medium"]:
        return "#FF9800"  # Orange
    else:
        return "#2196F3"  # Blue

# CSV columns for data collection
CSV_COLUMNS = [
    "timestamp",
    "prompt_text",
    "coding",
    "reasoning",
    "plain_language_conversion",
    "math",
    "factual",
    "creative_tone",
    "summary"
]

# Path to data collection file
DATA_FILE = "data/collected_prompts.csv"
