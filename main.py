import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# 環境変数からLINE Messaging APIの設定値を取得
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("2003969131")
LINE_CHANNEL_SECRET = os.getenv("2360bd36b3c2e5a794e0834b4ddd5fc2")

app = FastAPI()

# LINE Bot APIクライアントのインスタンス化
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.get("/")
def root():
    return {"title": "Hello World"}

@app.post("/webhook")
async def line_webhook(request: Request):
    # リクエストボディと署名を取得
    body = await request.body()
    signature = request.headers.get('X-Line-Signature')

    # 署名の検証とイベントハンドラの呼び出し
    try:
        handler.handle(body.decode('utf-8'), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    except LineBotApiError as e:
        raise HTTPException(status_code=500, detail=f"Line Bot API error: {e}")
    
    return JSONResponse(content={"status": "success"})

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    # ユーザーからのテキストメッセージに基づいて応答
    user_message = event.message.text

    if user_message == "こんにちは":
        response_message = "こんにちは！いかがお過ごしですか？"
    elif user_message == "こんばんは":
        response_message = "こんばんは！素敵な夜をお過ごしください。"
    else:
        response_message = "申し訳ありません、よく理解できませんでした。"

    # 応答メッセージの送信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response_message)
    )
