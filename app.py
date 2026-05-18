from flask import Flask, render_template, request, jsonify
from aes_engine import process_aes_verbose_json
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/process", methods=["POST"])
def process():

    payload = request.json

    result = process_aes_verbose_json(
        json.dumps(payload)
    )

    return jsonify(json.loads(result))

if __name__ == "__main__":
    app.run(debug=True)
