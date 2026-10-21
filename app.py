from flask import Flask, send_from_directory, jsonify
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

JENKINS_URL = "http://localhost:8080"
JENKINS_USER = ""
JENKINS_TOKEN = ""

@app.route("/")
def dashboard():
    return send_from_directory(".", "index.html")

@app.route("/api/builds")
def builds():
    try:
        response = requests.get(
            f"{JENKINS_URL}/job/Build-Performance-Analyzer/api/json",
            params={"tree": "builds[number,result,duration,timestamp]"},
            auth=HTTPBasicAuth(JENKINS_USER, JENKINS_TOKEN),
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        return jsonify([
            {
                "number": f"#{b['number']}",
                "status": b.get("result") or "RUNNING",
                "duration": round(b.get("duration", 0) / 1000),
                "timestamp": b.get("timestamp")
            }
            for b in data.get("builds", [])
        ])
    except requests.RequestException as error:
        return jsonify({"error": str(error)}), 502

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)