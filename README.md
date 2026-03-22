# Phase 1: Prompt Intent Classifier MVP

## Overview

This is Phase 1 of the Prompt Intent Classifier project - a multi-label prompt intent classification system.

**Current Status**: MVP with Google Gemini API backend (free tier)

## What It Does

Analyzes prompts and scores them across **six dimensions**:

1. **Coding** - Code generation, debugging, algorithms, implementation
2. **Reasoning** - Logical deduction, analysis, step-by-step thinking
3. **Plain Language/Conversion** - Rewrite, simplify, translate, paraphrase
4. **Math** - Calculations, proofs, algebra, probability, equations
5. **Factual** - Information retrieval, real-world facts, research
6. **Creative/Tone** - Jokes, stories, poetry, style, marketing copy

Each dimension is scored from **0.0 to 1.0**, where:
- **0.9-1.0** = Primary demand
- **0.7-0.9** = Strong secondary demand
- **0.4-0.7** = Moderate presence
- **0.1-0.4** = Minor support
- **0.0-0.1** = Not present

## Setup & Installation

### Prerequisites
- Python 3.8+
- Google Gemini API key (free tier available)

### Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up API key:
Get your free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

Then set the environment variable:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

Or create a `.env` file in the project root:
```
GEMINI_API_KEY=your-api-key-here
```

## Usage

### Run the Streamlit App

```bash
streamlit run phase1_streamlit_app.py
```

The app will open at `http://localhost:8501`

### Using the App

1. **Enter a prompt** in the text area
2. **Click "Analyze"** to get scores
3. **Review results**:
   - Dimension-by-dimension scores
   - Summary of primary intent
   - Top 2 dimensions

### Data Collection

Analyzed prompts are automatically saved to `data/collected_prompts.csv` for future model training. This data is essential for Phase 3.

## Project Structure

```
AiProject_PromptDraft/
├── phase1_streamlit_app.py    # Main UI
├── phase1_classification_api.py # Claude API wrapper
├── config.py                    # Rubric and configuration
├── requirements.txt             # Python dependencies
├── data/
│   └── collected_prompts.csv   # Collected training data
└── README_PHASE1.md            # This file
```

## Files Overview

### `config.py`
Defines the classification rubric with:
- Dimension definitions and descriptions
- Example prompts for each dimension
- Score interpretation thresholds
- CSV column structure

### `phase1_classification_api.py`
Handles Google Gemini API communication:
- `analyze_prompt()` - Analyzes a prompt using Gemini
- `format_scores_for_display()` - Formats results for UI
- Uses zero-shot prompting with clear rubric

### `phase1_streamlit_app.py`
Streamlit UI providing:
- Interactive prompt input
- Real-time analysis visualization
- Score display with progress bars
- Automatic data collection
- Statistics dashboard

## Architecture

```
User Input → Streamlit UI → Gemini API
                                ↓
                        Scores (0-1 per dimension)
                                ↓
                            Display Results
                                ↓
                        Save to CSV (Phase 2 training data)
```

## Next Steps

- **Phase 2**: Collect 500+ labeled prompts
- **Phase 3**: Fine-tune DistilBERT model on collected data
- **Phase 4**: Replace Claude API with trained model in FastAPI backend
- **Phase 5**: Polish UI and optimize for production

## Troubleshooting

### "ModuleNotFoundError: No module named 'google'"
Install the module: `pip install google-generativeai`

### "GEMINI_API_KEY not found"
Make sure your API key is set:
- Get a free key from [Google AI Studio](https://aistudio.google.com/app/apikey)
- Via environment variable: `export GEMINI_API_KEY="..."`
- Via `.env` file in project root

### Gemini API errors
Check:
- API key is valid
- You have available quota (free tier has rate limits)
- Network connectivity

## Training Data Column Definitions

The `collected_prompts.csv` file contains:
- `timestamp` - ISO format timestamp of analysis
- `prompt_text` - Original prompt analyzed
- `coding` - Score for coding dimension (0.0-1.0)
- `reasoning` - Score for reasoning dimension
- `plain_language_conversion` - Score for conversion
- `math` - Score for math dimension
- `factual` - Score for factual dimension
- `creative_tone` - Score for creative/tone dimension
- `summary` - Gemini's interpretation of primary intent

## Performance Notes

- Average analysis takes 1-3 seconds (API dependent)
- Quality is good with Gemini's zero-shot capabilities
- Free tier has rate limits but sufficient for development
- No model download/caching needed

## License

Part of Prompt Intent Classifier project.
