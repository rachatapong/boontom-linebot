from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from apscheduler.schedulers.background import BackgroundScheduler
import os

app = Flask(__name__)

# LINE credentials
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
group_id = os.getenv("LINE_GROUP_ID")  # ตั้งค่ากลุ่มเป้าหมายใน Secrets

# ตั้งเวลาส่งข้อความอัตโนมัติ
scheduler = BackgroundScheduler()

def send_daily_reminder():
    message = "📌 แจ้งเตือนเวรประจำวัน โปรดตรวจสอบความพร้อมในการปฏิบัติหน้าที่"
    line_bot_api.push_message(group_id, TextSendMessage(text=message))

def send_weekly_meeting_reminder():
    message = "📣 แจ้งเตือนประชุมประจำสัปดาห์ วันศุกร์ เวลา 10.00 น."
    line_bot_api.push_message(group_id, TextSendMessage(text=message))

# ตั้งเวลา
scheduler.add_job(send_daily_reminder, 'cron', hour=7, minute=30)       # ทุกวันเวลา 07:30
scheduler.add_job(send_weekly_meeting_reminder, 'cron', day_of_week='fri', hour=9, minute=0)  # ทุกวันศุกร์ 09:00
scheduler.start()

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
    text = event.message.text.strip()
    if text == "เมนู":
        reply = "📋 เมนู\n- แจ้งเวร\n- แจ้งประชุม\n- ติดต่อเจ้าหน้าที่"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

if __name__ == "__main__":
    app.run()
