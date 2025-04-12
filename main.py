from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("hXHOaQ65S+r4cpbKmXzrMxbtlphJLA79vsUuFkTFGfsEtBSV3nIVpgzSAZYW6W/WzVLn6Lpo55Ui5yuwr5OevRVTvi3Y9oS6LyHW/J3OBByXTuGG5spPKkDiciZboEblCCXNMwUQpByTEh/ToybGgAdB04t89/1O/w1cDnyilFU="))
handler = WebhookHandler(os.getenv("0ee3cbdeffb9dd17ffbaec295e369fae"))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text.strip()
    if msg == "เมนู":
        reply = "📋 เมนู\n- แจ้งเหตุ\n- แจ้งเวร\n- ติดต่อเจ้าหน้าที่"
    else:
        reply = f"คุณพิมพ์ว่า: {msg}"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
