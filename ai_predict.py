import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get OpenRouter API Key from .env
API_KEY = os.getenv("OPENROUTER_API_KEY")


def predict_health(glucose, haemoglobin, cholesterol):

    # AI Prompt
    prompt = (
        "You are a medical prediction system.\n\n"
        "Analyze these blood test values:\n\n"
        "Glucose: " + str(glucose) + "\n"
        "Haemoglobin: " + str(haemoglobin) + "\n"
        "Cholesterol: " + str(cholesterol) + "\n\n"
        "Return ONLY one short medical risk prediction sentence.\n"
        "Do not explain values.\n"
        "Do not use bullet points.\n"
        "Do not use headings.\n"
        "Keep response under 12 words."
    )

    try:

        # Send request to OpenRouter API
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer " + str(API_KEY),
                "Content-Type": "application/json"
            },
            json={
                "model": "openrouter/auto",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 50
            }
        )

        # Convert response to JSON
        data = response.json()

        # Extract AI-generated prediction
        if "choices" in data:

            result = data["choices"][0]["message"]["content"]

            result = result.strip()

            result = result.replace("\n", " ")

            return result

        else:

            return "Unable to generate prediction"

    except Exception as e:

        print("AI ERROR:", e)

        return "AI prediction unavailable"
