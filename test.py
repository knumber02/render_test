from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

@app.route("/login", methods=["PUT"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    token = hashlib.sha1((username + password).encode()).hexdigest()
    return jsonify({"token": token})

@app.route("/flag", methods=["PUT"])
def flag():
    data = request.get_json()
    print("✅ FLAG:", data["flag"])
    return jsonify({"ok": True})
