import data
import model as ml
import tensorflow as tf
import sqlite3
import os
import pickle
import numpy as np
import predict as prd
from flask import g
from threading import Thread
from configs import DEFINES
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter

# slack 연동 정보 입력 부분
SLACK_TOKEN = "xoxp-731556186981-731084486436-731108649988-fcf8d8ead796bbd0bfcfb6ecfc4259be"
SLACK_SIGNING_SECRET = "2fe2841d8f1d165d1bcbc1823a021159"

app = Flask(__name__)

slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


# Req. 2-2-1 대답 예측 함수 구현
def predict(text):
    print(text)
    print("res")
    res = prd.predict(text)
    return res

# Req 2-2-2. app.db 를 연동하여 웹에서 주고받는 데이터를 DB로 저장
conn = sqlite3.connect("app.db")
c = conn.cursor()

def insert(text):
    c.execute("INSERT INTO search_history(query) VALUES (?);", (text,))
    conn.commit()

def send_text(channel, app_text):
    slack_web_client.chat_postMessage(channel=channel, text=app_text)

# 챗봇이 멘션을 받았을 경우
@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]
    text = " ".join(list(text.split())[1:])
    # data = preprocess(text)
    print(text)
    app_text = predict(text)
    insert(app_text)
    t = Thread(target=send_text, args=(channel, app_text))
    t.start()

@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run()
