import google.generativeai as genai

# Set up your Gemini API key
genai.configure(api_key="AIzaSyDBgCYefWCn8GO9BVB9HYWOFR8pjZfMrZo")

def callGemini(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # print(f"Error: {str(e)}")
        pass