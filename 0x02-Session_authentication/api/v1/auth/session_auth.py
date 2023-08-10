#!/usr/bin/env python3
"""A module for session authentication"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """Session auth class that inherits from auth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Method to create a session and Session ID for user"""
        if user_id is None:
            return None
        if type(user_id) is not str:
            return None
        sess_id = uuid.uuid4()
        SessionAuth.user_id_by_session_id[sess_id] = user_id
        return sess_id
