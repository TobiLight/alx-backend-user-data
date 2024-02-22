#!/usr/bin/env python3
"""Basic Flask App"""

from typing import Tuple
from flask import Flask, Response, abort, jsonify, request
from auth import Auth


AUTH = Auth()

app = Flask(__name__)


@app.route("/", methods=['GET'], strict_slashes=False)
def index() -> Response:
    """Index route"""
    return jsonify({'message': 'Bienvenue'})


@app.route("/users", methods=["POST"], strict_slashes=False)
def user():
    """
    Registers a new user and returns a JSON response.
    """
    form = request.form
    email: str = form['email']
    password: str = form['password']

    try:
        user = AUTH.register_user(email=email, password=password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """Handles user login requests and creates sessions."""
    form = request.form
    email: str = form['email']
    password: str = form['password']

    session_id = None

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id,
                            httponly=True, secure=True)

        return response
    else:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
