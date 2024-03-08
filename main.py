import os
# import json
# import re
# import requests
# import asyncio
# import aiohttp
#import requests
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
import message_bot

# FastAPIのインスタンス作成
app = FastAPI()

# LINE Botに関するインスタンス作成
line_bot_api = LineBotApi(os.environ["2003969131"])
handler = WebhookHandler(os.environ["2360bd36b3c2e5a794e0834b4ddd5fc2"])

load_dotenv()

class LineModel(BaseModel):
    destination: str
    events: List


@app.get("/")
def root():
    return {"title": 'hello world'}

@app.post("/callback",summary="LINE Message APIからのコールバックです。",
    description="ユーザーからメッセージが送信された際、LINE Message APIからこちらのメソッドが呼び出されます。",
)
async def callback(request: Request, x_line_signature=Header(None)):

    body = await request.body()

    try:
        handler.handle(body.decode("utf-8"), x_line_signature)

    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="InvalidSignatureError")

    return "OK"

@handler.add(MessageEvent)
def handle_message(event):
    res_data = message_bot.send(event.message.text)
    line_bot_api.reply_message(event.reply_token, res_data)

# async def send_request():
#     while True:
#         async with aiohttp.ClientSession(connector=connector) as session:
#             async with session.get(deploy_url) as response:
#                 print(await response.text())
#         await asyncio.sleep(50)  # 50秒ごとにリクエストを送信


# @app.on_event("startup")
# async def startup_event():
#     asyncio.create_task(send_request())
