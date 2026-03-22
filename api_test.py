import google.generativeai as genai

# Paste your API key here
API_KEY = "AIzaSyD1Wn-xapY59dT2tHGVlV6i4NXmJXWCIDg"

# Configure the API key
genai.configure(api_key=API_KEY)

print("Models available for generation:")
# Loop through and list models that support text/media generation
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"- {m.name}")