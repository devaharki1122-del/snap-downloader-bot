from pyrogram import Client, filters
from flask import Flask, request, jsonify
from threading import Thread
import requests, os

# ==========================
# Telegram Bot Credentials
# ==========================
API_ID = 32052427
API_HASH = "d9e14b1e99ac33e20d41479a47d2622f"
BOT_TOKEN = "8116636234:AAHHh3BDKuiCChfhNbafx05OWyTTeFuUDYY"

bot = Client("snap_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ==========================
# Flask App
# ==========================
app = Flask(__name__)

@app.route("/send", methods=["POST"])
def send_message():
    data = request.json
    chat_id = data.get("chat_id")
    message = data.get("message")
    if chat_id and message:
        try:
            bot.send_message(chat_id, message)
            return jsonify({"status": "success", "message": message})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    return jsonify({"status": "error", "message": "chat_id or message missing"})

@app.route("/snap", methods=["POST"])
def snap():
    data = request.json
    chat_id = data.get("chat_id")
    url = data.get("url")
    if chat_id and url:
        try:
            #  
            r = requests.get(url)
            if r.status_code == 200:
                filename = "snap_video.mp4"
                with open(filename, "wb") as f:
                    f.write(r.content)
                #    Telegram
                with open(filename, "rb") as f:
                    bot.send_video(chat_id, f, caption=" Snap Video")
                os.remove(filename)
                return jsonify({"status": "success", "message": "Video sent!"})
            else:
                return jsonify({"status": "error", "message": "Invalid URL or video not accessible"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    return jsonify({"status": "error", "message": "chat_id or url missing"})

# ==========================
# Run  + Flask
# ==========================
def run_flask():
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    Thread(target=bot.run).start()
    run_flask()