#!/usr/bin/env python3
"""An authentication class for basic auth"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """Authentication class to manage API auth"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Routes that require authorization"""
        if not path or not excluded_paths:
            return True
        if path[-1] != "/":
            slash_path = path + "/"
        else:
            slash_path = path
        if path in excluded_paths or slash_path in excluded_paths:
            return False
        if path not in excluded_paths or slash_path not in excluded_paths:
            return True

    def authorization_header(self, request=None) -> str:
        """Check creds in request header"""
        if not request:
            return None
        if request.headers.get("Authorization") is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """Return user object"""
        return None

    def session_cookie(self, request=None):
        """Method that returns a cookie value from a request
        """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
