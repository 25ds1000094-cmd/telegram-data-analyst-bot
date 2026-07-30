from flask import Flask
import threading
import os
import json

from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters
)

from ai_agent import ask_ai
from logger import save_log



async def message_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    question = update.message.text


    save_log({

        "event":"question_received",

        "question":question

    })


    try:

        answer = ask_ai(question)


    except Exception as e:

        answer = {
            "error":str(e)
        }


    result={

        "answer":answer,

        "log_url":
        "YOUR_PUBLIC_LOG_URL_HERE"

    }


    save_log({

        "event":"response_sent",

        "response":result

    })


    await update.message.reply_text(

        json.dumps(result)

    )



app = Application.builder().token(

    os.environ["TELEGRAM_TOKEN"]

).build()



app.add_handler(

    MessageHandler(

        filters.TEXT,

        message_handler

    )

)



print("Bot running...")

web_app = Flask(__name__)


@web_app.route("/")
def home():
    return "Bot is running"


def run_web():
    web_app.run(
        host="0.0.0.0",
        port=10000
    )


threading.Thread(
    target=run_web
).start()

app.run_polling()
