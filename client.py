import google.generativeai as genai
import os

# Set API key
GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")  # Or set manually
genai.configure(api_key=GOOGLE_GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-pro")

# Generate response
response = model.generate_content("What is coding?")
print(response.text)
