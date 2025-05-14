import os
import subprocess
import requests
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

# /start command
@bot.on_message(filters.command("start"))
async def start_command(client, message):
    image_url = "https://graph.org/file/4e8a1172e8ba4b7a0bdfa.jpg"
    await message.reply_photo(
        photo=image_url,
        caption="**Welcome to the Docker Image Bot!**\n\nUse `/download` to receive the latest Docker image.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Join Channel", url="https://t.me/Opleech_WD")]
        ])
    )

# /download command to dynamically fetch docker image, export & send
@bot.on_message(filters.command("download"))
async def download_docker_image(client, message):
    status = await message.reply("Pulling Docker image, please wait...")

    try:
        # Step 1: Pull Docker image
        subprocess.run(["docker", "pull", "labani/stream:latest"], check=True)

        # Step 2: Create container and export as stream.tar
        subprocess.run(["docker", "create", "--name", "tempcontainer", "labani/stream:latest"], check=True)
        subprocess.run("docker export tempcontainer > stream.tar", shell=True, check=True)
        subprocess.run(["docker", "rm", "tempcontainer"], check=True)

        # Step 3: Send the file
        await client.send_document(
            chat_id=message.chat.id,
            document="stream.tar",
            caption="✅ Docker image exported and sent!"
        )

        await status.edit("✅ Done! Docker image sent successfully.")
    except subprocess.CalledProcessError as e:
        await status.edit("❌ Failed to process Docker image.\nCheck logs or Docker status.")
    except Exception as ex:
        await status.edit(f"❌ Unexpected error: {ex}")

# Run Flask and Bot
def run_web():
    web_app.run(host='0.0.0.0', port=PORT)

if __name__ == '__main__':
    threading.Thread(target=run_web).start()
    bot.run()
