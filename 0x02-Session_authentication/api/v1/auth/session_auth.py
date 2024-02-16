#!/usr/bin/env python3
"""
Session Authentication module
"""
from ..auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    Session Authentication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates and returns a Session ID for a user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        from uuid import uuid4

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID based on a Session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None

        return str(self.user_id_by_session_id.get(session_id))

    def current_user(self, request=None):
        """
        Returns a User instance based on a cookie value.
        """
        user_session_cookie = self.session_cookie(request)
        user_id = self.user_id_by_session_id.get(user_session_cookie)
        if user_id:
            user = User.get(user_id)
            return user

    def destroy_session(self, request=None):
        """
        Deletes the user session / logout.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)

        if session_id is None:
            return False

        if user_id is None:
            return False

        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]

        return True
