import os
import asyncio
import threading
from flask import Flask
import whisper
from pyrogram import Client, filters

# Render को एक्टिव रखने के लिए हल्का वेब सर्वर
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is Active!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host="0.0.0.0", port=port)

# Telegram API सेटिंग्स
API_ID = int(os.environ.get("API_ID", "12345678"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

app = Client("AutoCaptionBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# AI Whisper Model (मोबाइल/फ्री सर्वर के लिए 'tiny' या 'base' मॉडल बेस्ट है)
model = whisper.load_model("tiny")

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text("👋 **नमस्ते!** मुझे कोई भी वीडियो या ऑडियो भेजें, मैं ऑटोमैटिक कैप्शन जनरेट कर दूँगा।")

@app.on_message((filters.video | filters.audio | filters.voice) & filters.private)
async def process_media(client, message):
    status_msg = await message.reply_text("📥 फाइल डाउनलोड हो रही है...")
    file_path = None
    try:
        file_path = await message.download()
        await status_msg.edit_text("🎙️ AI कैप्शन तैयार कर रहा है...")

        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, lambda: model.transcribe(file_path))
        caption = result.get("text", "").strip()

        if not caption:
            await status_msg.edit_text("❌ ऑडियो में कोई आवाज़ नहीं मिली।")
            return

        formatted_caption = f"📝 **Auto Caption:**\n\n{caption[:1000]}"

        if message.video:
            await message.reply_video(video=file_path, caption=formatted_caption)
        elif message.audio or message.voice:
            await message.reply_audio(audio=file_path, caption=formatted_caption)

        await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text(f"⚠️ एरर आया: `{str(e)}`")
    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    app.run()
  
