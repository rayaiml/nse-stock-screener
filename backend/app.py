
from flask import Flask, jsonify, request
from flask_cors import CORS
from scanner import scan

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return {"status": "OK"}

@app.route("/scan")
def run_scan():
    filters = {"volume": request.args.get("volume", "1") == "1"}
    return jsonify(scan(filters))

if __name__ == "__main__":
    app.run()
