from flask import Flask, request, jsonify
from mnemonic import Mnemonic

app = Flask(__name__)
mnemo = Mnemonic("english")

@app.route('/check', methods=['POST'])
def check():
    data = request.get_json()
    words = data.get('words', '').strip()
    words_list = words.split()

    if len(words_list) not in [11, 12]:
        return jsonify({"error": "Please provide 11 or 12 words"}), 400

    valid_phrases = []

    if len(words_list) == 11:
        for w in mnemo.wordlist:
            phrase = words_list + [w]
            phrase_str = ' '.join(phrase)
            if mnemo.check(phrase_str):
                valid_phrases.append(phrase_str)
    else:
        phrase_str = ' '.join(words_list)
        if mnemo.check(phrase_str):
            valid_phrases.append(phrase_str)

    if not valid_phrases:
        return jsonify({"valid_phrases": [], "message": "No valid phrase found."})

    return jsonify({"valid_phrases": valid_phrases})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
