from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

@app.route("/")
def index():
    return "🚀 Backend en ligne"

# --- POST : reçoit la newsletter depuis n8n ---
@app.route("/newsletter", methods=["POST"])
def receive_newsletter():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Aucune donnée reçue"}), 400

        # n8n envoie souvent [{"output": {...}}]
        if isinstance(data, list) and "output" in data[0]:
            data = data[0]["output"]

        # Sauvegarde dans un fichier local (Railway garde ça tant que le conteneur tourne)
        with open(DATA_FILE, "w") as f:
            json.dump(data, f)

        print("✅ Donnée reçue :", data["titre"])
        return jsonify({"status": "success", "message": "Newsletter enregistrée"}), 200

    except Exception as e:
        print("❌ Erreur :", e)
        return jsonify({"status": "error", "message": str(e)}), 500


# --- GET : permet à Streamlit de récupérer la dernière newsletter ---
@app.route("/newsletter", methods=["GET"])
def get_newsletter():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        return jsonify(data)
    else:
        return jsonify({"message": "Aucune newsletter enregistrée"}), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
