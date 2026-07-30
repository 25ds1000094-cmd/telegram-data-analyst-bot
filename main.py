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


app.run_polling()
