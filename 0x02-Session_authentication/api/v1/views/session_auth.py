#!/usr/bin/env python3
"""
Module that handles all routes for the Session authentication
"""
from os import getenv
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """
    POST /api/v1/auth_session/login
    JSON body:
      - email
      - password
    Return:
      - User object JSON represented
      - 404 if no User found
    """
    email = request.args.get('email')
    password = request.args.get('password')

    if email is None or len(email) == 0:
        return jsonify({"error": "email missing"}), 400

    if password is None or len(password) == 0:
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if len(users) <= 0:
        return jsonify({"error": "no user found for this email"}), 404

    if not users[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    user_session_id = auth.create_session(getattr(users[0], 'id'))
    resp = jsonify(users[0].to_json())
    resp.set_cookie(getenv("SESSION_NAME"), user_session_id)

    return resp
