"""
Google Gemini API Integration for Prompt Intent Classification

This module handles communication with Google Gemini API to score prompts
across six dimensions using the defined rubric.
"""

import json
import os
from google import genai
from config import DIMENSIONS, DIMENSION_KEYS

# Check if we're using mock mode (for testing)
USE_MOCK_MODE = os.getenv("USE_MOCK_API", "false").lower() == "true"

# Initialize Gemini client
if not USE_MOCK_MODE:
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"Warning: Could not initialize Gemini client: {e}")
        print("Falling back to mock mode for testing")
        USE_MOCK_MODE = True
else:
    client = None

# System prompt with rubric
SYSTEM_PROMPT = """You are an expert prompt analyzer that classifies prompts across six dimensions of requirement/demand:

1. **Coding**: Code generation, debugging, algorithms, implementation, syntax
2. **Reasoning**: Logical deduction, analysis, step-by-step thinking, problem decomposition
3. **Plain Language/Conversion**: Rewrite, simplify, translate, paraphrase, clarification
4. **Math**: Calculation, proof, algebra, probability, equations, statistics
5. **Factual**: Information retrieval, explanation of real-world facts, research
6. **Creative/Tone**: Jokes, stories, poetry, style adaptation, marketing copy, humor

For each prompt, you will:
1. Score each dimension from 0.0 to 1.0 indicating "How much does this prompt require this capability?"
2. Provide a brief one-line summary of the primary intent
3. Identify the top 1-2 dimensions

**Scoring Guidelines:**
- 0.9-1.0: This is the primary demand of the prompt
- 0.7-0.9: Strong secondary demand
- 0.4-0.7: Moderate presence
- 0.1-0.4: Minor/supporting presence
- 0.0-0.1: Not present

**Important**: A single prompt can score high on multiple dimensions. This is a multi-label classification task.

Return your response as valid JSON only, with no additional text."""

def create_analysis_prompt(prompt_text: str) -> str:
    """Create the analysis prompt with rubric context."""

    rubric_text = "Here are detailed definitions and examples:\n\n"
    for key in DIMENSION_KEYS:
        dim = DIMENSIONS[key]
        rubric_text += f"**{dim['label']}**: {dim['description']}\n"
        rubric_text += f"Examples: {', '.join(dim['examples'][:2])}\n\n"

    return f"""{rubric_text}Analyze this prompt:

"{prompt_text}"

Return ONLY valid JSON (no markdown, no code blocks, no additional text) with this exact structure:
{{
  "scores": {{
    "coding": 0.0,
    "reasoning": 0.0,
    "plain_language_conversion": 0.0,
    "math": 0.0,
    "factual": 0.0,
    "creative_tone": 0.0
  }},
  "summary": "One sentence describing the primary intent",
  "top_labels": ["dimension1", "dimension2"]
}}"""

def analyze_prompt(prompt_text: str) -> dict:
    """
    Analyze a prompt using Gemini API.

    Args:
        prompt_text: The prompt to analyze

    Returns:
        Dictionary with keys:
        - scores: dict of dimension -> score (0-1)
        - summary: str describing primary intent
        - top_labels: list of top 1-2 dimensions
    """

    try:
        # Use mock data when API key is not available
        if USE_MOCK_MODE:
            return {
                "scores": {
                    "coding": 0.85,
                    "reasoning": 0.3,
                    "plain_language_conversion": 0.1,
                    "math": 0.2,
                    "factual": 0.15,
                    "creative_tone": 0.05
                },
                "summary": "Mock analysis - API key not configured",
                "top_labels": ["coding"]
            }

        # Prepare the full prompt with system context
        full_prompt = f"{SYSTEM_PROMPT}\n\n{create_analysis_prompt(prompt_text)}"

        # Call Gemini API with models.generate_content
        # Use an explicit model name that is available for your
        # API version/region. "gemini-1.5-flash" is the standard
        # fast, low-cost model; adjust here if you want a different one.
        response = client.models.generate_content(
            model="gemini-flash-latest",  # Adjust model name as needed
            contents=full_prompt,
        )

        # Extract the response text
        response_text = response.text.strip()

        # Parse JSON response
        result = json.loads(response_text)

        # Validate all dimensions are present
        for dim_key in DIMENSION_KEYS:
            if dim_key not in result["scores"]:
                result["scores"][dim_key] = 0.0

        # Ensure scores are floats between 0 and 1
        for dim_key in DIMENSION_KEYS:
            score = float(result["scores"][dim_key])
            result["scores"][dim_key] = max(0.0, min(1.0, score))

        return result

    except json.JSONDecodeError as e:
        print(f"Error parsing Gemini response: {e}")
        # Return default scores on error
        return {
            "scores": {k: 0.0 for k in DIMENSION_KEYS},
            "summary": "Error analyzing prompt",
            "top_labels": [],
            "error": str(e)
        }
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return {
            "scores": {k: 0.0 for k in DIMENSION_KEYS},
            "summary": "Error analyzing prompt",
            "top_labels": [],
            "error": str(e)
        }

def format_scores_for_display(result: dict) -> dict:
    """
    Format analysis results for display in UI.

    Args:
        result: Output from analyze_prompt()

    Returns:
        Dictionary with formatted display information
    """
    return {
        "scores": result["scores"],
        "summary": result.get("summary", ""),
        "top_labels": result.get("top_labels", []),
        "display_labels": [
            DIMENSIONS[label]["label"] for label in result.get("top_labels", [])
        ]
    }
