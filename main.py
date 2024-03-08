from linebot.exceptions import LineBotApiError
from linebot.models import TextSendMessage
from linebot import LineBotApi
from fastapi import FastAPI, Query, Header, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from starlette.exceptions import HTTPException
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import json

load_dotenv()

# FastAPIのインスタンス作成
app = FastAPI()

# # LINE Botに関するインスタンス作成
line_bot_api = LineBotApi("2003969131")
handler = WebhookHandler("2360bd36b3c2e5a794e0834b4ddd5fc2")

# LINE Bot APIの初期化（環境変数からアクセストークンを取得する想定）
line_bot_api = LineBotApi(
    'l9mxZXowA7nMVUh0Ro2DZlGq6kezJfvY3bpheuI0i1XfK6xUhHcHdqAh8i9W0rbVC7p/u4R2w4eX4oY/7F5jUOvInvGqsm5AjwHGQPuasuuxnflF9T2AN8kfuMrA06K+AjETChr+3jiy35z srQhwcQdB04t89/1O/w1cDnyilFU=')


def handle_message(message_text: str):
    # メッセージ内容に基づいた条件分岐
    if message_text == "こんにちは":
        return "こんにちは！どういたしまして。"
    else:
        return "申し訳ありません、理解できませんでした。"


@app.post("/")
async def webhook(request: Request):
    body = await request.body()
    # JSONデータを解析
    data = json.loads(body.decode("utf-8"))

    # メッセージイベントの解析
    for event in data["events"]:
        if event["type"] == "message" and event["message"]["type"] == "text":
            # テキストメッセージの内容を取得
            message_text = event["message"]["text"]
            # 条件に基づく返答メッセージの決定
            if message_text == "こんにちは":
                response_message = [
                    {
                        "message":  [
                            {
                                "type": "text",
                                "text": "hello",
                            }
                        ]
                    }
                ]
            else:
                response_message = [
                    {
                        "message": [
                            {
                                "type": "text",
                                "text": "hello world"
                            }
                        ]
                    }
                ]

            try:
                # LINEユーザーに返答メッセージを送信
                line_bot_api.reply_message(
                    event['replyToken'],
                    TextSendMessage(text=response_message)
                )
            except LineBotApiError as e:
                # エラーハンドリング
                print(f"Failed to send reply message: {e}")

    return {"status": "success"}

# ---------------------------------------------------------------------------------------------------------
# FastAPIのインスタンス作成
# app = FastAPI()

# # LINE Botに関するインスタンス作成
# line_bot_api = LineBotApi("2003969131")
# handler = WebhookHandler("2360bd36b3c2e5a794e0834b4ddd5fc2")


# @app.get("/")
# def root():
#     return {"title": 'hello world'}


# @app.post("/webhook")
# async def line_webhook(message):
#     print("===========================================================================")
#     global A

#     if message == "こんにちは":
#         print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#         A = [
#             {
#                 "message": [
#                     {
#                         "type": "text",
#                         "text": "hello",
#                     }
#                 ]
#             }
#         ]
#     elif message == "こんばんわ":
#         A = {
#             "message":
#                 {
#                     "type": "text",
#                     "text": "good night",
#                 }
#         }
#     else:
#         A = {
#             "message":
#                 {
#                     "type": "text",
#                     "text": "hello world"
#                 }
#         }
#     return A


# @handler.add(MessageEvent, text=TextMessage)
# def handle_message(event):
#     text = event.message.text

#     line_bot_api.reply_message(event.reply_token, A)
