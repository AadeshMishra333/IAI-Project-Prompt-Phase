import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load variables from .env.example (template-style local config)
load_dotenv(".env.example")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env.example")

# Configure the API key
genai.configure(api_key=API_KEY)

print("Models available for generation:")
# Loop through and list models that support text/media generation
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"- {m.name}")