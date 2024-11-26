import google.generativeai as genai
import os

API_KEY = os.getenv("API_KEY")

# Set up your Gemini API key
genai.configure(api_key=API_KEY)

def callGemini(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # print(f"Error: {str(e)}")
        pass