#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, abort, jsonify, request
from flask_cors import (CORS)


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

if getenv('AUTH_TYPE') is not None:
    if getenv('AUTH_TYPE') == 'basic_auth':
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    elif getenv('AUTH_TYPE') == 'session_auth':
        from api.v1.auth.session_auth import SessionAuth
        auth = SessionAuth()
    else:
        from api.v1.auth.auth import Auth
        auth = Auth()


@app.before_request
def before_request():
    """
    Authenticates a user before processing requests.
    """
    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login/'
    ]
    if auth is None or not auth.\
            require_auth(request.path, excluded_paths):
        return

    if auth.authorization_header(request) is None and\
            auth.session_cookie(request) is None:
        abort(401)

    if auth.current_user(request) is None:
        abort(403)

    request.current_user = auth.current_user(request)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Unauthorized handler"""
    response = jsonify({"error": "Unauthorized"})
    response.status_code = error.code
    return response


@app.errorhandler(403)
def forbidden(error) -> str:
    """Forbidden handler"""
    response = jsonify({"error": "Forbidden"})
    response.status_code = error.code
    return response


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=int(port), debug=True)
