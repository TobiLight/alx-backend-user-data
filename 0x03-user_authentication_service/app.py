#!/usr/bin/env python3
"""Basic Flask App"""

from typing import Tuple
from flask import Flask, Response, jsonify, request
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
        return jsonify({"email": email, "message": "user created"}), 201
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
