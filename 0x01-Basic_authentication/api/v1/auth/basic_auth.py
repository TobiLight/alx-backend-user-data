#!/usr/bin/env python3
"""
Basic Auth module
"""
import base64
import binascii
from typing import TypeVar
from ..auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """
    Basic Authentication
    """

    def extract_base64_authorization_header(self, authorization_header: str)\
            -> str:
        """
        Extracts and returns the Base64 part from a Basic authentication
        header.
        """
        if authorization_header is None or\
                not isinstance(authorization_header,
                               str) or not\
                authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ", 1)[1]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """
        Decodes and returns the decoded value of a Base64 string
        base64_authorization_header
        """
        if not base64_authorization_header:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            # Decode and return as UTF-8
            return base64.b64decode(base64_authorization_header).\
                decode('utf-8')
        except (UnicodeDecodeError, binascii.Error):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        Extracts the user email and password from the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ":" not in decoded_base64_authorization_header:
            return None, None

        user_email, user_password = decoded_base64_authorization_header.split(
            ":", 1)

        return (user_email, user_password)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on the email and password provided.
        """
        if not isinstance(user_email, str) or user_email is None:
            return None

        if not isinstance(user_pwd, str) or user_pwd is None:
            return None

        user = User.search({'email': user_email})

        if not user:
            return None

        if not user[0].is_valid_password(user_pwd):
            return None

        return user[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves and returns the authenticated User instance for a request.
        """

        if request is None:
            request = g.get('request')

        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return None

        extracted_base64 = self.extract_base64_authorization_header(
            authorization_header)
        if not extracted_base64:
            return None

        decoded_base64 = self.decode_base64_authorization_header(
            extracted_base64)

        if not decoded_base64:
            return None

        user_email, user_password = self.extract_user_credentials(
            decoded_base64)

        if not user_email or not user_password:
            return None

        user = self.user_object_from_credentials(user_email, user_password)
        return user
