import os
import json
import re
import requests
import asyncio
import aiohttp
from fastapi import FastAPI, Query, Header, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent
from starlette.exceptions import HTTPException

load_dotenv()
# FastAPIのインスタンス作成
app = FastAPI()

# LINE Botに関するインスタンス作成
line_bot_api = LineBotApi("2003969131")
handler = WebhookHandler("2360bd36b3c2e5a794e0834b4ddd5fc2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"title": 'hello world'}


@app.post("/webhook")
async def line_webhook(message: str = Query(None)):  # Queryのデフォルト値をNoneに設定
    print("===========================================================================")
    global A

    if message == "こんにちは":
        A = {
            "message":
                {
                    "type": "text",
                    "text": "hello",
                }
        }
    elif message == "こんばんわ":
        A = {
            "message":
                {
                    "type": "text",
                    "text": "good night",
                }
        }
    else:
        A = {
            "message":
                {
                    "type": "text",
                    "text": "hello world"
                }
        }
    return A


@handler.add(MessageEvent)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token, A)

# async def send_request():
#     while True:
#         async with aiohttp.ClientSession(connector=connector) as session:
#             async with session.get(deploy_url) as response:
#                 print(await response.text())
#         await asyncio.sleep(50)  # 50秒ごとにリクエストを送信


# @app.on_event("startup")
# async def startup_event():
#     asyncio.create_task(send_request())
