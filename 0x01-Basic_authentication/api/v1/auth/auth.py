#!/usr/bin/env python3
"""An authentication class for basic auth"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Authentication class to manage API auth"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Routes that require authorization"""
        return False

    def authorization_header(self, request=None) -> str:
        """Check creds in request header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Return user object"""
        return None
