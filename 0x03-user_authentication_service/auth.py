#!/usr/bin/env python3
"""Auth module"""

from db import DB
from bcrypt import hashpw, gensalt
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Returns a salted, hashed password, which is a byte string."""
    return hashpw(password.encode('utf-8'), gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user and returns the created User object.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            User: The created User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(
                email, hashed_password.decode('utf-8'))
            return new_user
        raise ValueError(f"User {email} already exists")