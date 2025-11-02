from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

@app.route('/newsletter', methods=['POST'])
def receive_newsletter():
    data = request.get_json()
    print("Reçu :", data)

    if not data or "newsletter" not in data:
        return jsonify({"error": "Invalid data"}), 400

    with open("data.json", "w") as f:
        json.dump(data["newsletter"], f, ensure_ascii=False, indent=2)

    return jsonify({"status": "received"}), 200

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)


