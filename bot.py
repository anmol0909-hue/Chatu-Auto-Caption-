import os
from pyrogram import Client, filters
from google import genai

# Environment Variables से क्रेडेंशियल्स लें
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")

# Gemini AI Client
client_ai = genai.Client(api_key=GOOGLE_API_KEY)

# Pyrogram Bot Client
app = Client(
    "AutoCaptionBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text("👋 **नमस्ते!** मैं आपका Auto Caption Bot हूँ। मुझे कोई भी फोटो या मैसेज भेजें, मैं शानदार कैप्शन लिख दूँगा।")

@app.on_message((filters.photo | filters.document | filters.text) & filters.private)
async def generate_caption(client, message):
    if message.text and message.text.startswith("/"):
        return

    status = await message.reply_text("✨ AI कैप्शन तैयार कर रहा है...")
    try:
        user_prompt = "Create a catchy, engaging social media caption with trending hashtags for a post."
        if message.caption:
            user_prompt += f" Context: {message.caption}"
            
        response = client_ai.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt,
        )
        caption_text = response.text

        await message.reply_text(f"📝 **Auto Caption:**\n\n{caption_text}")
        await status.delete()
    except Exception as e:
        await status.edit_text(f"⚠️ एरर: `{str(e)}`")

if __name__ == "__main__":
    print("Bot is starting...")
    app.run()
    
