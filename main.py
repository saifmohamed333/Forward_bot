from telethon.sync import TelegramClient, events
import asyncio
import base64
import os
import re
from getpass import getpass

# استرجاع بيانات الجلسة المشفرة من متغير البيئة وفكها
session_data = os.getenv("SESSION_DATA")
if session_data:
    with open("session_name.session", "wb") as f:
        decoded_data = base64.b64decode(session_data)
        f.write(decoded_data)
        print("✅ تم فك التشفير وحفظ الجلسة بنجاح!")

# إعدادات API و التليجرام
api_id = 26283926
api_hash = 'fcd8c080125fad9062c9bc7d9cb2ca2d'
source_channel = -1002304519486
destination_bot = 'TradeWiz_Solbot'

client = TelegramClient('session_name', api_id, api_hash)

# دالة استخراج العقد وإرساله فقط (بسرعة)
@client.on(events.NewMessage(chats=source_channel))
async def forward_contract_only(event):
    try:
        raw_text = event.message.message or event.message.raw_text or ""
    except Exception:
        raw_text = ""

    if not raw_text.strip():
        print("⚠️ لا يوجد نص يمكن تحليله.")
        return

    print(f"📩 النص المستلم:\n{raw_text}")

    lines = raw_text.splitlines()
    contract = None
    for line in lines:
        if re.match(r"^[a-zA-Z0-9]{30,}pump$", line.strip()):
            contract = line.strip()
            break

    if contract:
        print(f"✅ تم استخراج العقد: {contract}")
        try:
            await client.send_message(destination_bot, contract)
            print("📤 تم إرسال العقد للبوت.")
        except Exception as e:
            print(f"❌ خطأ أثناء الإرسال: {e}")
    else:
        print("⚠️ لم يتم العثور على عقد في الرسالة.")

async def main():
    await client.start()
    print("🚀 البوت يعمل الآن، في انتظار الرسائل...")
    await client.run_until_disconnected()

async def restart_client():
    while True:
        try:
            await main()
        except Exception as e:
            print(f"🚫 خطأ في الاتصال أو التنفيذ، إعادة المحاولة بعد 5 ثوانٍ... {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(restart_client())
