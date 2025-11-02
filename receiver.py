from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "🚀 Backend en ligne"

@app.route("/newsletter", methods=["POST"])
def receive_newsletter():
    data = request.get_json()
    print("✅ Donnée reçue :", data)  # Log pour Railway
    return jsonify({"status": "success", "message": "Newsletter reçue"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
