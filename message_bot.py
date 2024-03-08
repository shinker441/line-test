from linebot.models import TextSendMessage

def send(message: str):
    """
    引数のメッセージに応答するメッセージを返します。
    
    Parameters
    ----------
    message : str
        Messaging APIで受信したメッセージです。
        
    Returns
    ----------
    management_bot : FlexSendMessage or TextSendMessage
    """

    # デフォルトの応答を設定
    result = TextSendMessage(text="ごめんなさい、理解できませんでした。")
    
    if message == "こんにちは":
        result = TextSendMessage(text="hello")
    
    return result
