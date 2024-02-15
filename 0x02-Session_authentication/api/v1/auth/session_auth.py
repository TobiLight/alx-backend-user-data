#!/usr/bin/env python3
"""
Session Authentication module
"""
from ..auth.auth import Auth


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
