#!/usr/bin/env python3
"""Basic Flask application"""
from flask import Flask, jsonify, request
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home_route():
    """Method to render a json of the homepage"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user_route():
    """Function that implements logic to register a new user"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        new_user = AUTH.register_user(email, password)
        return jsonify({"email": new_user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
