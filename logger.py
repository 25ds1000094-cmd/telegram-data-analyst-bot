import json
import os
from datetime import datetime


LOG_FILE = "logs/run.jsonl"


def save_log(data):

    os.makedirs("logs", exist_ok=True)

    data["time"] = str(datetime.now())

    with open(LOG_FILE, "a") as f:
        f.write(
            json.dumps(data)
            + "\n"
        )
