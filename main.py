from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage,
    JoinEvent, MemberJoinedEvent,
    TextSendMessage
)
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

# ✅ ต้อนรับสมาชิกใหม่ พร้อมแสดงชื่อ
@handler.add(MemberJoinedEvent)
def welcome_new_member(event):
    for member in event.joined.members:
        user_id = member.user_id
        try:
            profile = line_bot_api.get_profile(user_id)
            display_name = profile.display_name
        except:
            display_name = "เพื่อนใหม่"

        message = f"🎉 ยินดีต้อนรับคุณ {display_name} เข้าสู่กลุ่ม SPYPOLICE นักสืบบุญตอมครับ!"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
        )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
