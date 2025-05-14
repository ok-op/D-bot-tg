import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from flask import Flask, jsonify

load_dotenv()
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID"))  # Your Telegram user ID
PORT = 3000

app = Client("docker_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Flask app
app = Flask(__name__)
app.json.ensure_ascii = False

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "🎬 Welcome to the docker image downloader bot",
        "description": "📡 This bot fetches the latest docker image posts them to Telegram.",
        "developer": "👨‍💻 Developed by WOODcraft",
        "channel": "📢 Join our channel: @Opleech_WD"
    })


@app.on_message(filters.command("upload") & filters.user(OWNER_ID))
async def upload_tar(client, message):
    file_path = "stream.tar"
    if os.path.exists(file_path):
        await message.reply_document(
            document=file_path,
            caption="Here is your extracted Docker image!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬇️ Download", url=f"https://t.me/{app.me.username}?start=download")]
            ])
        )
    else:
        await message.reply("The stream.tar file was not found!")

if __name__ == '__main__':
# Start the Flask app
    app.run(host='0.0.0.0', port=PORT)
