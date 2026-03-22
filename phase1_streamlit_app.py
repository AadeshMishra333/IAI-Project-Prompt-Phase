"""
Streamlit UI for Prompt Intent Classifier

A multi-label prompt intent classification system that analyzes prompts
across six dimensions: coding, reasoning, plain language conversion,
math, factual knowledge, and creative/tone.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os
from phase1_classification_api import analyze_prompt, format_scores_for_display
from config import DIMENSIONS, DIMENSION_KEYS, CSV_COLUMNS, DATA_FILE, interpret_score, get_color_for_score

# Page configuration
st.set_page_config(
    page_title="Prompt Intent Classifier",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        border-radius: 10px;
        padding: 20px;
        background-color: #f0f2f6;
        margin: 10px 0;
    }
    .score-bar-container {
        margin: 15px 0;
        padding: 10px;
        background-color: #ffffff;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("🎯 Prompt Intent Classifier")
st.markdown("""
Analyze prompts to understand what capabilities they demand.
This system scores each prompt across **six dimensions**:
- **Coding**: Code generation, debugging, algorithms
- **Reasoning**: Logical deduction, analysis, step-by-step thinking
- **Plain Language/Conversion**: Rewrite, simplify, translate
- **Math**: Calculations, proofs, equations
- **Factual**: Information, real-world facts, research
- **Creative/Tone**: Jokes, stories, poetry, style
""")

st.divider()

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Settings")
    st.markdown("### Model Settings")
    st.info("Using Google Gemini Flash with optimized rubric for accurate multi-label classification")

    st.markdown("### Data Collection")
    if st.checkbox("Enable data collection", value=True):
        st.success("✅ Data collection enabled")
        st.caption("Analyzed prompts will be saved for future model training")
    else:
        st.warning("⚠️ Data collection disabled")

# Main input section
st.header("📝 Analyze a Prompt")

col1, col2 = st.columns([4, 1])

with col1:
    prompt_input = st.text_area(
        "Enter a prompt to analyze",
        placeholder="Example: Write a Python function to calculate fibonacci numbers...",
        height=120,
        label_visibility="collapsed"
    )

with col2:
    st.empty()  # Placeholder for spacing
    analyze_button = st.button(
        "🔍 Analyze",
        use_container_width=True,
        type="primary",
        key="analyze_btn"
    )
    
def save_to_csv(prompt_text: str, result: dict):
    """Save analysis result to CSV for data collection."""
    try:
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)

        # Prepare row data
        row_data = {
            "timestamp": datetime.now().isoformat(),
            "prompt_text": prompt_text,
            **result["scores"],
            "summary": result.get("summary", "")
        }

        # Create DataFrame
        new_row_df = pd.DataFrame([row_data])

        # Append to CSV or create new one
        if os.path.exists(DATA_FILE):
            existing_df = pd.read_csv(DATA_FILE)
            updated_df = pd.concat([existing_df, new_row_df], ignore_index=True)
            updated_df.to_csv(DATA_FILE, index=False)
        else:
            new_row_df.to_csv(DATA_FILE, index=False)

    except Exception as e:
        print(f"Error saving to CSV: {e}")

# Analysis section
if analyze_button:
    if not prompt_input.strip():
        st.error("Please enter a prompt to analyze")
    else:
        with st.spinner("🤖 Analyzing prompt with Gemini..."):
            try:
                # Get analysis from Gemini API
                result = analyze_prompt(prompt_input.strip())

                # Format for display
                display_result = format_scores_for_display(result)

                # Check if there was an error
                if "error" in result:
                    st.error(f"Error analyzing prompt: {result['error']}")
                else:
                    # Save to CSV if enabled
                    if st.session_state.get("collection_enabled", True):
                        save_to_csv(prompt_input, result)

                    # Display results
                    st.success("✅ Analysis complete!")

                    # Summary section
                    st.subheader("📊 Summary")
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"**Primary Intent**: {display_result['summary']}")
                    with col2:
                        if display_result['display_labels']:
                            st.metric(
                                "Top Dimensions",
                                ", ".join(display_result['display_labels'][:2])
                            )

                    st.divider()

                    # Scores display
                    st.subheader("📈 Dimension Scores")

                    # Create columns for score display
                    cols = st.columns(2)
                    for idx, dim_key in enumerate(DIMENSION_KEYS):
                        col_idx = idx % 2
                        with cols[col_idx]:
                            score = display_result['scores'][dim_key]
                            label = DIMENSIONS[dim_key]['label']
                            interpretation = interpret_score(score)

                            # Create progress bar
                            st.write(f"**{label}**")
                            st.progress(
                                score,
                                text=f"{score:.2f} ({interpretation})"
                            )

                    st.divider()

                    # Detailed breakdown
                    st.subheader("🔍 Detailed Breakdown")
                    scores_df = pd.DataFrame(
                        [
                            {
                                "Dimension": DIMENSIONS[k]['label'],
                                "Score": f"{display_result['scores'][k]:.2f}",
                                "Level": interpret_score(display_result['scores'][k]),
                                "Description": DIMENSIONS[k]['description']
                            }
                            for k in DIMENSION_KEYS
                        ]
                    )
                    st.dataframe(
                        scores_df,
                        use_container_width=True,
                        hide_index=True,
                    )

                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("💾 Save Analysis", use_container_width=True):
                            st.success("✅ Saved! This analysis will be used for model training.")

                    with col2:
                        if st.button("📋 Copy JSON", use_container_width=True):
                            import json
                            json_str = json.dumps(result, indent=2)
                            st.code(json_str, language="json")

                    with col3:
                        if st.button("🔄 New Analysis", use_container_width=True):
                            st.rerun()

            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")

st.divider()

# History and statistics section
st.header("📊 Statistics & History")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📈 Data Collection")
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE)
            st.metric("Prompts Collected", len(df))
            st.metric("Total Analyses", len(df))
        except:
            st.info("No data collected yet")
    else:
        st.info("Data file will be created on first save")

with col2:
    st.subheader("📝 About")
    st.info("""
    This is Phase 1 of the Prompt Intent Classifier project.
    - Currently using Google Gemini API for accurate zero-shot classification
    - Later phases will include fine-tuned models for faster inference
    - Your analyses help train the system
    """)

# Footer
st.divider()
st.caption("🚀 Prompt Intent Classifier v0.1 | Phase 1: MVP with Google Gemini API")
