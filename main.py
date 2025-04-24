from flask import Flask, request, abort
import os
from datetime import datetime
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# ชุดเวร
duty_teams = [
    [  # ชุดที่ 1
        'ร.ต.อ.บุญมา ไสยสิทธิ์',
        'ร.ต.ท.เทพรัศมี ปรักมาศ',
        'ด.ต.อำพล สุทธิโสกเชือก',
        'จ.ส.ต.รชฏพงศ์ อ้นศรีวงศ์',
        'ส.ต.อ.สมพร น้อยบาท'
    ],
    [  # ชุดที่ 2
        'ร.ต.อ.สายันต์ คู่กระสังข์',
        'ด.ต.ชัยรัตน์ มาตย์วิเศษ',
        'ส.ต.อ.นิติ ศรีลาดเลา',
        'ส.ต.อ.วชิรวิทย์ กระจ่างจันทร์'
    ],
    [  # ชุดที่ 3
        'ร.ต.อ.วินัย สิงห์อ้น',
        'ด.ต.อุดม โตนวุธ',
        'ด.ต.ก้องเกียรติ แก้วมัจฉา',
        'ด.ต.จงลักษณ์ ข่าขันมะลี',
        'ส.ต.ท.กฤษฎา ทำสุนา'
    ]
]

# 🧠 คำนวณชุดเวรวันนี้
def get_duty_message():
    today = datetime.now()
    start_date = datetime(2025, 4, 3)
    diff_days = (today.date() - start_date.date()).days
    team_index = diff_days % 3
    team = duty_teams[team_index]

    date_th = today.strftime("%A %d/%m/%Y")
    message = f"📢 แจ้งเตือนเข้าเวร\n🗓️ วันที่ {date_th}\nเวลา 08.00 น. ถึง 08.00 น. วันถัดไป\n\nชุดเข้าเวร:\n" + \
              "\n".join([f"- {name}" for name in team]) + "\n\nบุญเตือนรายงานครับเจ้านาย"
    return message

@app.route("/", methods=["GET"])
def home():
    return "Boontom LINE Bot is active!"

@app.route("/webhook", methods=['POST'])
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
    user_message = event.message.text.strip().lower()
    if user_message == "/เวร":
        reply_text = get_duty_message()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )
