from dotenv import load_dotenv
from fastapi import FastAPI, BackgroundTasks, Header, HTTPException, Request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextSendMessage, TextMessage
import json
import os

load_dotenv()

app = FastAPI()

# ApiRoot Health Check


@app.get("/")
def api_root():
    return {"message": "LINEBOT-API-TALK-A3RT Healthy"}


# LINE Messaging APIの準備
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.post("/")
async def callback(request: Request, background_tasks: BackgroundTasks):
    body = await request.body()
    data_json = json.loads(body)
    print(data_json)
    token = data_json["events"][0]["replyToken"]

    background_tasks.add_task(handle_message, data_json)
    # INFO:     147.92.150.193:0 - "POST / HTTP/1.1" 200 OK
# '{"destination":"U94530c9340e4fe7045c73b0450a86980","events":[{"type":"message","message":{"type":"text","id":"498465752207065399","quoteToken":"NWEg2cuIKkGODtObK5YL2QL9Wzmws-kDYj2uaNvijNxWI2vy14zHX81qEGGJV9cEISHUB98TS3J02J1rBMCWyJRSvTRbUaam8CZ8M-6SLIagRdg74EQqq7Cf9DbUNF1_XtD1opq0xnUBVkrIwLYnPQ","text":"hello"},"webhookEventId":"01HRG5WXPRTKEDGEPCKG680NXS","deliveryContext":{"isRedelivery":false},"timestamp":1709940045104,"source":{"type":"user","userId":"Ufb88bea97c59e74464a5666598703157"},"replyToken":"16222b97f3ea474e8b062c0d6028c2ac","mode":"active"}]}'
    return {"message": "ok"}

# LINE Messaging APIからのメッセージイベントを処理


@handler.add(MessageEvent)
def handle_message(data_json):
    message = TextMessage(text=data_json["events"][0]["message"]["text"])
    line_bot_api.reply_message(data_json["events"][0]["replyToken"], message)

# ----------------------------------------------------------------------------------------------------------
# from linebot.exceptions import LineBotApiError
# from linebot.models import TextSendMessage
# from linebot import LineBotApi
# from fastapi import FastAPI, Query, Header, Request
# from fastapi.responses import FileResponse
# from fastapi.middleware.cors import CORSMiddleware
# from dotenv import load_dotenv
# from linebot import LineBotApi, WebhookHandler
# from linebot.exceptions import InvalidSignatureError
# from starlette.exceptions import HTTPException
# from linebot.models import MessageEvent, TextMessage, TextSendMessage
# import json

# load_dotenv()

# # FastAPIのインスタンス作成
# app = FastAPI()

# # # LINE Botに関するインスタンス作成
# line_bot_api = LineBotApi("")
# handler = WebhookHandler("")

# # LINE Bot APIの初期化（環境変数からアクセストークンを取得する想定）
# line_bot_api = LineBotApi(
#     'l9mxZXowA7nMVUh0Ro2DZlGq6kezJfvY3bpheuI0i1XfK6xUhHcHdqAh8i9W0rbVC7p/u4R2w4eX4oY/7F5jUOvInvGqsm5AjwHGQPuasuuxnflF9T2AN8kfuMrA06K+AjETChr+3jiy35z srQhwcQdB04t89/1O/w1cDnyilFU=')


# def handle_message(message_text: str):
#     # メッセージ内容に基づいた条件分岐
#     if message_text == "こんにちは":
#         return [
#                     {
#                         "message":  [
#                             {
#                                 "type": "text",
#                                 "text": "hello",
#                             }
#                         ]
#                     }
#                 ]
#     else:
#         return [
#                     {
#                         "message": [
#                             {
#                                 "type": "text",
#                                 "text": "hello world"
#                             }
#                         ]
#                     }
#                 ]


# @app.post("/")
# async def webhook(request: Request):
#     body = await request.body()
#     # JSONデータを解析
#     data = json.loads(body.decode("utf-8"))

#     # メッセージイベントの解析
#     for event in data["events"]:
#         if event["type"] == "message" and event["message"]["type"] == "text":
#             # テキストメッセージの内容を取得
#             message_text = event["message"]["text"]
#             # 条件に基づく返答メッセージの決定
#             response_message = handle_message(message_text)

#             try:
#                 # LINEユーザーに返答メッセージを送信
#                 line_bot_api.reply_message(
#                     event['replyToken'],
#                     TextSendMessage(text=response_message)
#                 )
#             except LineBotApiError as e:
#                 # エラーハンドリング
#                 print(f"Failed to send reply message: {e}")

#     return {"status": "success"}

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
