"""
Test script for Phase 1 - Prompt Intent Classifier

Tests the Claude API integration with sample prompts.
"""

import sys
import json
from phase1_classification_api import analyze_prompt, format_scores_for_display
from config import DIMENSIONS, DIMENSION_KEYS

# Sample test prompts covering different dimensions
TEST_PROMPTS = [
    "write a python function to calculate fibonacci numbers",
    "explain how photosynthesis works step by step",
    "simplify this sentence for a 5-year-old: The phenomenon of quantum entanglement is fascinating",
    "solve this equation: 2x + 5 = 15",
    "what is the capital of France?",
    "tell me a funny joke about programming"
]

def test_analyze_prompt(prompt_text: str):
    """Test analyzing a single prompt."""
    print(f"\n{'='*80}")
    print(f"PROMPT: {prompt_text}")
    print(f"{'='*80}")

    try:
        result = analyze_prompt(prompt_text)

        if "error" in result:
            print(f"❌ ERROR: {result['error']}")
            return False

        # Display results
        print(f"\n✅ Analysis successful\n")
        print(f"Summary: {result.get('summary', 'N/A')}")
        print(f"Top Labels: {', '.join(result.get('top_labels', []))}")
        print(f"\nScores:")
        print("-" * 60)

        # Find max score for highlighting expected dimension
        max_score = 0
        max_dim = None
        for dim_key in DIMENSION_KEYS:
            score = result["scores"][dim_key]
            dim_label = DIMENSIONS[dim_key]["label"]
            print(f"  {dim_label:25} {score:.2f}")
            if score > max_score:
                max_score = score
                max_dim = dim_key

        print("-" * 60)
        print(f"Highest: {DIMENSIONS[max_dim]['label']} ({max_score:.2f})")

        return True

    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("=" * 80)
    print("🧪 PHASE 1 TEST SUITE - Prompt Intent Classifier")
    print("=" * 80)
    print(f"\nTesting {len(TEST_PROMPTS)} sample prompts...\n")

    passed = 0
    failed = 0

    for i, prompt in enumerate(TEST_PROMPTS, 1):
        print(f"\n[{i}/{len(TEST_PROMPTS)}] Testing prompt...")
        if test_analyze_prompt(prompt):
            passed += 1
        else:
            failed += 1

    # Summary
    print(f"\n\n{'='*80}")
    print("📊 TEST SUMMARY")
    print(f"{'='*80}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
    print(f"{'='*80}\n")

    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
