#!/usr/bin/env python3
"""Basic Flask App"""
from flask import Flask, Response, abort, jsonify, redirect, request
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
        response.status_code = 200
        response.set_cookie('session_id', session_id)

        return response
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout():
    """Handles user logout requests and invalidates sessions."""
    session_id = request.cookies.get("session_id")

    if not session_id:
        return abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        return abort(403)

    AUTH.destroy_session(user.id)

    response = redirect("/")
    response.delete_cookie("session_id")
    return response


@app.route("/profile", methods=['GET'])
def profile():
    """Retrieves and returns user profile information."""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> Response:
    """
    Handles password reset requests and generates tokens.
    """
    form = request.form
    email: str = form['email']
    reset_token = None

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify(
        {"email": email, "reset_token": reset_token})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """Handles password reset requests and updates passwords."""
    form = request.form
    email = form['email']
    reset_token = form['reset_token']
    new_password = form['new_password']

    try:
        AUTH.update_password(reset_token, password=new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
