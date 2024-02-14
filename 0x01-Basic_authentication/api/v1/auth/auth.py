#!/usr/bin/env python3
"""
Auth module
"""
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
