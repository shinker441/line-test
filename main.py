from fastapi import FastAPI, BackgroundTasks, Header, HTTPException, Request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextSendMessage, TextMessage
import json
import os

app = FastAPI()

# ApiRoot Health Check


@app.get("/")
def api_root():
    return {"message": "LINEBOT-API-TALK-A3RT Healthy"}


# LINE Messaging APIの準備
CHANNEL_ACCESS_TOKEN = "l9mxZXowA7nMVUh0Ro2DZlGq6kezJfvY3bpheuI0i1XfK6xUhHcHdqAh8i9W0rbVC7p/u4R2w4eX4oY/7F5jUOvInvGqsm5AjwHGQPuasuuxnflF9T2AN8kfuMrA06K+AjETChr+3jiy35zsrQhwcQdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "2360bd36b3c2e5a794e0834b4ddd5fc2"

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.post("/")
async def callback(request: Request,background_tasks:BackgroundTasks):
    body = await request.body()
    data_json = json.loads(body)
    print(data_json)
    if data_json["events"]!=None:
        token = data_json["events"][0]["replyToken"]
        background_tasks.add_task(handle_message,data_json)
    else :
        return 0

    return {"message": "ok"}

# LINE Messaging APIからのメッセージイベントを処理


@handler.add(MessageEvent)
def handle_message(data_json):
    message = TextMessage(text=data_json["events"][0]["message"]["text"])
    line_bot_api.reply_message(data_json["events"][0]["replyToken"], message)