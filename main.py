import os
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

res_data = ""
load_dotenv()
# FastAPIのインスタンス作成
app = FastAPI(title="kris'slinebot-sample",
              description="This is sample of kris's LINE Bot.")

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
    return {"title": app.title, "description": app.description}


@app.post("/")
async def root(message: str = Query(None)):  # Queryのデフォルト値をNoneに設定
    if message == "こんにちは":
        res_data = "message:こんにちは！ようこそ"
        return res_data

    elif message == "質問してもいいですか":
        res_data = "message:もちろんです。何かお困りですか？"
        return res_data
    else:
        res_data = "すいません。よくわかりません。"
        return res_data


@handler.add(MessageEvent)
def handle_message(event):
    """
    LINE Messaging APIのハンドラより呼び出される処理です。
    受け取ったメッセージに従い返信メッセージを返却します。

    Parameters
    ----------
    event : MessageEvent
        送信されたメッセージの情報です。
    """

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


'''
------------------------------------------------------------------------------------------------------
@app.get(
    "/resources/{directory}/{file}",
    summary="静的ファイルの取得用です。",
    description="指定したパスのファイルをレスポンスします。",
)
def resources(directory: str, file: str):

    return FileResponse("./app/resources/" + directory + "/" + file)
------------------------------------------------------------------------------------------------------
'''
