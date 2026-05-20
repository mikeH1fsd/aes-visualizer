from flask import Flask, render_template, request, jsonify

from aes_engine import (
    process_aes_verbose_json,
    process_key_expansion_json
)

import json

app = Flask(__name__)

# =========================================
# HOME
# =========================================

@app.route("/")
def home():

    return render_template("index.html")

# =========================================
# AES PROCESS API
# =========================================

@app.route("/api/process", methods=["POST"])
def process():

    payload = request.json

    result = process_aes_verbose_json(
        json.dumps(payload)
    )

    return jsonify(json.loads(result))

# =========================================
# KEY EXPANSION API
# =========================================

@app.route("/api/key-expansion", methods=["POST"])
def key_expansion():

    payload = request.json

    result = process_key_expansion_json(
        json.dumps(payload)
    )

    return jsonify(json.loads(result))

# =========================================
# RUN
# =========================================

if __name__ == "__main__":

    app.run(debug=True)
