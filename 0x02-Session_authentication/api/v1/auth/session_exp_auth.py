#!/usr/bin/env python3
"""
SessionExp Module
"""
from os import getenv
from ..auth.session_auth import SessionAuth


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
        pass
