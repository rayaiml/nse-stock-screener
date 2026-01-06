from flask import Flask, jsonify
from flask_cors import CORS
from scanner import scan

app = Flask(__name__)
CORS(app)

@app.route("/scan")
def run_scan():
    return jsonify(scan())

if __name__ == "__main__":
    app.run()
