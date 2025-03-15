from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

# Hardcoded correct password for testing
CORRECT_PASSWORD = "1234"

@app.route('/verify-password', methods=['POST'])
def verify_password():
    data = request.get_json()
    password = data.get("password")

    if password == CORRECT_PASSWORD:
        return jsonify({"message": "✅ Correct Password!"})
    else:
        return jsonify({"message": "❌ Incorrect Password!"}), 401

if __name__ == '__main__':
    app.run(debug=True)
