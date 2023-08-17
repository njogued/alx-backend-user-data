#!/usr/bin/env python3
"""Basic Flask application"""
from flask import Flask, jsonify, request, abort
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home_route():
    """Method to render a json of the homepage"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user_route():
    """Function that implements logic to register a new user"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        new_user = AUTH.register_user(email, password)
        return jsonify({"email": new_user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """Function to implement login logic"""
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        sess_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', sess_id)
    else:
        abort(401)
    return response


@app.route('/profile', methods=['GET'], strict_slashes=False)
def get_profile():
    """Function that returns a user's profile"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
