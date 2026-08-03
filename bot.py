import os
import asyncio
import threading
from flask import Flask
import google.generativeai as genai
from pyrogram import Client, filters

# Flask Web Server
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is Live!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host="0.0.0.0", port=port)

# API Keys
API_ID = int(os.environ.get("API_ID", "12345678"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Gemini Config
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

app = Client("AutoCaptionBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text("👋 **नमस्ते!** मुझे कोई भी फोटो या फाइल भेजें, मैं आकर्षक कैप्शन बना दूँगा।")

@app.on_message((filters.photo | filters.document) & filters.private)
async def generate_caption(client, message):
    status = await message.reply_text("✨ AI कैप्शन तैयार कर रहा है...")
    try:
        response = model.generate_content("Create a short, engaging social media caption with trending hashtags for this upload.")
        caption_text = response.text
        await message.reply_text(f"📝 **Auto Caption:**\n\n{caption_text}")
        await status.delete()
    except Exception as e:
        await status.edit_text(f"⚠️ एरर: `{str(e)}`")

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    app.run()
    
