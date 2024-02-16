#!/usr/bin/env python3
"""
SessionExp Module
"""
from os import getenv
from ..auth.session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    Session Expiration Class
    """

    def __init__(self) -> None:
        """Initialize new instance"""
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates a session id for the user.
        """
        session_id = super().create_session(user_id)

        if type(session_id) != str:
            return None

        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns a User ID based on a Session ID
        """
        if session_id is None:
            return None

        if session_id not in self.user_id_by_session_id:
            return None

        if self.session_duration <= 0:
            return None

        session_dict = self.user_id_by_session_id[session_id]

        if session_dict['created_at'] is None:
            return None

        curr_time = datetime.now()

        if session_dict['created_at'] +\
                timedelta(seconds=self.session_duration) < curr_time:
            return None

        return session_dict['user_id']
