import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")


def predict_health(glucose, haemoglobin, cholesterol):

    prompt = (
        "You are a medical assistant.\n\n"
        "Analyze these blood test results.\n\n"
        "Glucose: " + str(glucose) + "\n"
        "Haemoglobin: " + str(haemoglobin) + "\n"
        "Cholesterol: " + str(cholesterol) + "\n\n"
        "Give a short possible health risk prediction in one sentence."
    )

    try:

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
                ]
            }
        )

        print(response.status_code)
        print(response.text)

        data = response.json()

        result = data['choices'][0]['message']['content']

        return result

    except Exception as e:

        print("ERROR:", e)

        return "AI prediction unavailable"