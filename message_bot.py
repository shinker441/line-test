from linebot.models import (TextSendMessage)

def send(message: str):
    """
    引数のメッセージに応答するメッセージを返します。

    Parameters
    ----------
    message : str
        Messaging APIで受信したメッセージです。

    Returns
    ----------
    managent_bot : FlexSendMessage or TextSendMessage
    """

    if message=="こんにちは":
        result = TextSendMessage(text="hello")
    return result