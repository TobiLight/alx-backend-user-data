#!/usr/bin/env python3
"""Auth module"""

from typing import Union
import bcrypt
from db import DB
from bcrypt import hashpw, gensalt, checkpw
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Returns a salted, hashed password, which is a byte string.

    Args:
        password (str): The password to be hashed

    Returns:
        Hashed password as a byte string

    """
    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    """
    Returns a string representation of a new UUID
    """
    from uuid import uuid4
    return str(uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates user login credentials.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            bool: True if credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(bytes(password, 'utf-8'), user.hashed_password.
                           encode())
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Creates a new session for the user and returns the session ID.

        Args:
            email (str): The user's email address.

        Returns:
            str: The newly generated session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user_id=user.id, session_id=session_id)

            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Retrieves the user associated with the given session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            User | None: The corresponding User object or None if not found.
        """
        if not session_id:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Invalidates the session for the given user.

        Args:
            user_id (int): The ID of the user whose session to invalidate.
        """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates and stores a password reset token for a user.

        Args:
            email (str): The user's email address.

        Returns:
            str: The generated password reset token.

        Raises:
            ValueError: If the user with the provided email is not found.
        """
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user_id=user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError
