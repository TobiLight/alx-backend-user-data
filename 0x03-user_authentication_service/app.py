#!/usr/bin/env python3
"""Basic Flask App"""

from flask import Flask, Response, jsonify

app = Flask(__name__)


@app.route("/", methods=['GET'], strict_slashes=False)
def index() -> Response:
    """Index route"""
    return jsonify({'message': 'Bienvenue'})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
