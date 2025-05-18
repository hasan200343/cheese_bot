from flask import Flask
from threading import Thread
import datetime

app = Flask('')


@app.route('/')
def home():
    print(f"[{datetime.datetime.now()}] Ping received!")
    return "I'm alive!", 200


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()
