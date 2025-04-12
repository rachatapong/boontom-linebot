from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

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
elif msg == "ส่งรูป":
    image_url = "https://drive.google.com/file/d/0ByZ8Hukn1W5_UWdvTmtYbEJLNTQ/view?usp=sharing&resourcekey=0-c18u5rbMyoDuerIP9L9J0A"  # เปลี่ยนลิงก์รูปตรงนี้
    line_bot_api.reply_message(
        event.reply_token,
        [
            TextSendMessage(text="📸 นี่คือภาพที่คุณร้องขอ"),
            ImageSendMessage(
                original_content_url=image_url,
                preview_image_url=image_url
            )
        ]
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
