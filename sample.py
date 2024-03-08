from fastapi import FastAPI, Header, Request, HTTPException
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
import os

# 環境変数の読み込み
load_dotenv()

# FastAPIのインスタンス作成
app = FastAPI()

# LINE Botに関するインスタンス作成
line_bot_api = LineBotApi("l9mxZXowA7nMVUh0Ro2DZlGq6kezJfvY3bpheuI0i1XfK6xUhHcHdqAh8i9W0rbVC7p/u4R2w4eX4oY/7F5jUOvInvGqsm5AjwHGQPuasuuxnflF9T2AN8kfuMrA06K+AjETChr+3jiy35zsrQhwcQdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("2360bd36b3c2e5a794e0834b4ddd5fc2")

@app.get("/")
def root():
    return {"title": 'hello world'}

@app.post("/callback")
async def callback(request: Request):

    body = await request.body()
    print(body)
    return {"text","hello"}