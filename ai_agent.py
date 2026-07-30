import os
import requests
import json


def ask_ai(question):

    token = os.environ["AI_PIPE_TOKEN"]

    response = requests.post(

        "https://aipipe.org/openai/v1/chat/completions",

        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },

        json={

            "model": "gpt-4o-mini",

            "messages": [
                {
                    "role": "system",
                    "content": """
                    You are a data analyst.
                    Answer the user's question.
                    Return ONLY valid JSON.
                    """
                },
                {
                    "role": "user",
                    "content": question
                }
            ]

        }

    )


    print("STATUS:", response.status_code)
    print("RAW RESPONSE:", response.text)


    data = response.json()


    # OpenAI compatible response
    if "choices" in data:
        text = data["choices"][0]["message"]["content"]

    # Some AI Pipe responses use output
    elif "output" in data:
        text = data["output"]

    # Some return message
    elif "message" in data:
        text = data["message"]

    else:
        return {
            "error": "Unknown AI response format",
            "raw": data
        }


    try:
        return json.loads(text)

    except:

        return {
            "answer": text
        }
