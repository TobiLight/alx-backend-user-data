#!/usr/bin/env python3
"""
Auth module
"""
from os import getenv
from typing import List, TypeVar
from flask import request


class Auth:
    """API Authenticaion"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required for a given path.
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        path = path.rstrip("/")

        for excluded_path in excluded_paths:
            excluded_path = excluded_path.rstrip("/")
            if excluded_path.endswith("*"):
                if path.startswith(excluded_path[:-1]):
                    return False
            else:
                if path == excluded_path:
                    return False

        if path not in excluded_paths:
            return True

        return False

    def authorization_header(self, request=None) -> str:
        """
        Extracts the authorization header from the request.
        """
        if request is None or 'Authorization' not in request.headers:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on the request.
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns a cookie value from a request.
        """
        if request is not None:
            cookie_name = getenv('SESSION_NAME')
            return request.cookies.get(cookie_name)
