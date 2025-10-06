from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import time

app = Flask(__name__)
CORS(app)

# Simulated in-memory storage for temporary numbers and SMS
numbers_db = {}
sms_db = {}

def generate_temp_number():
    return f"+1555{random.randint(1000000,9999999)}"

@app.route("/api/get_number", methods=["POST"])
def get_number():
    number = generate_temp_number()
    session_id = str(random.randint(100000, 999999))
    numbers_db[session_id] = number
    # Simulate code sent (in real world, your provider would do this)
    code = str(random.randint(100000, 999999))
    sms_db[session_id] = {"number": number, "code": code, "timestamp": time.time()}
    return jsonify({"number": number, "session_id": session_id}), 200

@app.route("/api/get_sms", methods=["POST"])
def get_sms():
    session_id = request.json.get("session_id")
    sms = sms_db.get(session_id)
    if sms:
        # Simulate delay for SMS arrival
        if time.time() - sms["timestamp"] < 3:
            return jsonify({"sms": None}), 200
        return jsonify({"sms": f"Your WhatsApp code is {sms['code']}"}), 200
    return jsonify({"error": "Invalid session_id"}), 404

if __name__ == "__main__":
    app.run(debug=True)
