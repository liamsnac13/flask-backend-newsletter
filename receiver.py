from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "🚀 Backend en ligne"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)

