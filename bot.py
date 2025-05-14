import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from flask import Flask, jsonify
import threading

# Load .env variables
load_dotenv()
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID"))
PORT = 3000

# Pyrogram Bot Client
bot = Client("docker_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Flask App
web_app = Flask(__name__)
web_app.json.ensure_ascii = False

@web_app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "🎬 Welcome to the Docker image downloader bot",
        "description": "📡 This bot fetches the latest Docker image and posts them to Telegram.",
        "developer": "👨‍💻 Developed by WOODcraft",
        "channel": "📢 Join our channel: @Opleech_WD"
    })

# /start command with welcome image and button
@bot.on_message(filters.command("start"))
async def start_command(client, message):
    image_url = "https://graph.org/file/4e8a1172e8ba4b7a0bdfa.jpg"  # Change to your image URL or local path
    await message.reply_photo(
        photo=image_url,
        caption="**Welcome to the Docker Image Bot!**\n\nUse `/send` to receive the latest extracted image.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Join Channel", url="https://t.me/Opleech_WD")]
        ])
    )

# /send command (same as upload) - anyone can use
@bot.on_message(filters.command("send"))
async def send_tar(client, message):
    file_path = "stream.tar"
    if os.path.exists(file_path):
        await message.reply_document(
            document=file_path,
            caption="Here is your extracted Docker image!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬇️ Download", url=f"https://t.me/{(await client.get_me()).username}?start=download")]
            ])
        )
    else:
        await message.reply("The stream.tar file was not found!")

# Run both Flask and Bot together
def run_web():
    web_app.run(host='0.0.0.0', port=PORT)

if __name__ == '__main__':
    threading.Thread(target=run_web).start()
    bot.run()
