# import os
# import json
# import re
# import requests
# import asyncio
# import aiohttp
import requests
from fastapi import FastAPI, Query, Header, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent
from starlette.exceptions import HTTPException
from pydantic import BaseModel
from typing import List

# FastAPIのインスタンス作成
app = FastAPI()

# LINE Botに関するインスタンス作成
line_bot_api = LineBotApi("2003969131")
handler = WebhookHandler("2360bd36b3c2e5a794e0834b4ddd5fc2")

load_dotenv()
channelAccessToken = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LineModel(BaseModel):
    destination: str
    events: List


@app.get("/")
def root():
    return {"title": 'hello world'}


@app.post("/webhook")
async def line_webhook(request: LineModel):
    msg = request.events[0]["message"]["text"]
    replyToken = request.events[0]["replyToken"]

    print("ユーザ: %s" % msg)

    # global A

    # A= {
    #     "replyToken": body.replyToken,
    #     "messeages": [
    #         {
    #             "type": "text",
    #             "text": "hello",
    #         }
    #     ]
    # }
    # print(body)

    sendMsg = {"message": "recieved"}

    sendPostHead = {
        "Authorization": channelAccessToken
    }

    sendPostData = {
        "replyToken": replyToken,
        "messages": [
            {
                "type": "text",
                "text": sendMsg
            }
        ]
    }

    res = requests.post("https://api.line.me/v2/bot/message/reply",
                        headers=sendPostHead, json=sendPostData)

    print("linebotのレスポンス: %s" % res)

    return request

# @handler.add(MessageEvent)
# def handle_message(A):
#     line_bot_api.reply_message(A.replyToken, A)

# async def send_request():
#     while True:
#         async with aiohttp.ClientSession(connector=connector) as session:
#             async with session.get(deploy_url) as response:
#                 print(await response.text())
#         await asyncio.sleep(50)  # 50秒ごとにリクエストを送信


# @app.on_event("startup")
# async def startup_event():
#     asyncio.create_task(send_request())
