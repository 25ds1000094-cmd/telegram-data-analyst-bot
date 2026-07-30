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
You are a data analyst agent.

Follow these rules strictly:

1. Read the user's entire message carefully.
2. Solve the data analysis question.
3. The user message contains the exact JSON format they want.
4. Return ONLY the JSON object requested by the user.
5. Do not add explanations, markdown, comments, or extra text.
6. Match the requested JSON keys exactly.
7. If the user asks for {"state":"<state name>"}, return exactly that structure.
8. If the user asks for another structure, follow that structure instead.
9. For questions involving public datasets, use your knowledge of the dataset and perform the required analysis.
10. Your final output must always be valid JSON.
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


    try:
        data = response.json()

    except Exception:

        return {
            "error": "AI returned invalid response",
            "raw": response.text
        }


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


    except Exception:

        return {
            "error": "AI returned invalid JSON",
            "raw": text
        }
