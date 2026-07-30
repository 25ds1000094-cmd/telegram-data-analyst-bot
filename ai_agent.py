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

            "messages":[

                {
                    "role":"system",
                    "content":
                    """
                    You are a data analyst.

                    Answer the user's question.

                    Return ONLY valid JSON.
                    No markdown.
                    No explanation.
                    """
                },

                {
                    "role":"user",
                    "content":question
                }

            ]

        }

    )


    data=response.json()


    answer=data["choices"][0]["message"]["content"]


    return json.loads(answer)
