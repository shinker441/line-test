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
async def callback(request: Request, background_tasks: BackgroundTasks):
    body = await request.body()
    data_json = json.loads(body)
    print(data_json)

    # Check if "events" key exists and it is not an empty list
    if "events" in data_json and data_json["events"]:
        try:
            # Proceed knowing that data_json["events"] is not empty
            token = data_json["events"][0]["replyToken"]
            background_tasks.add_task(handle_message, data_json)
        except IndexError:
            # Handle the case where the list is shorter than expected
            print("Received 'events' list is shorter than expected.")
            return {"error": "Invalid event data."}
    else:
        print("No events found in the request body.")
        return {"error": "No events found."}

    return {"message": "ok"}


# LINE Messaging APIからのメッセージイベントを処理


@handler.add(MessageEvent)
def handle_message(data_json):
    # Extract the text from the incoming message
    incoming_text = data_json["events"][0]["message"]["text"]

    with open("faqs.json", "r", encoding="utf-8") as file:
        faqs = json.load(file)

    for item in faqs:
        # Assuming faqs is a list of dictionaries where each item has a question and answer
        # And you are checking if the incoming text matches any question in the FAQs
        if incoming_text.lower() in item["question"].lower():
            # Create a TextSendMessage object with the answer
            reply_message = TextSendMessage(text=item["answer"])
            line_bot_api.reply_message(
                data_json["events"][0]["replyToken"], reply_message)
            return  # Exit after sending the reply to avoid multiple replies

    # Optional: send a default reply if no FAQ match is found
    default_reply = TextSendMessage(
        text="Sorry, I don't have an answer to that question.")
    line_bot_api.reply_message(
        data_json["events"][0]["replyToken"], default_reply)
