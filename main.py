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

# ✅ ต้อนรับเพื่อนใหม่ที่เข้ากลุ่ม
@handler.add(MemberJoinedEvent)
def handle_member_joined(event):
    new_member = event.joined.members[0]
    user_id = new_member.user_id

    try:
        profile = line_bot_api.get_profile(user_id)
        display_name = profile.display_name
    except:
        display_name = "เพื่อนใหม่"

    welcome_text = f"สวัสดีครับคุณ {display_name} 🎉\nยินดีต้อนรับสู่กลุ่มของเรา"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=welcome_text)
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
