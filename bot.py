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
    return "Bot is Live and Active!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host="0.0.0.0", port=port)

# API Credentials
API_ID = int(os.environ.get("API_ID", "12345678"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")

# Gemini API Configure
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

# Gemini Model Config (ताज़ा मॉडल)
model = model = genai.GenerativeModel('gemini-1.5-flash')


app = Client("AutoCaptionBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text("👋 **नमस्ते!** मुझे कोई भी फोटो, फाइल या मैसेज भेजें, मैं सुंदर ऑटो-कैप्शन बनाकर दूँगा।")

@app.on_message((filters.photo | filters.document | filters.text) & filters.private)
async def generate_caption(client, message):
    if message.text and message.text.startswith("/"):
        return  # कमांड्स को इग्नोर करें

    status = await message.reply_text("✨ AI कैप्शन तैयार कर रहा है...")
    try:
        user_prompt = "Create a catchy, engaging social media caption with trending hashtags for a post."
        
        # अगर यूज़र ने साथ में कुछ टेक्स्ट भी भेजा है तो उसे संदर्भ में लें
        if message.caption:
            user_prompt += f" Context/Topic: {message.caption}"
            
        response = model.generate_content(user_prompt)
        caption_text = response.text

        await message.reply_text(f"📝 **Auto Caption:**\n\n{caption_text}")
        await status.delete()
    except Exception as e:
        await status.edit_text(f"⚠️ एरर आया: `{str(e)}`")

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    app.run()
    
