#!/usr/bin/env python3
"""A BASICAUTH class that inherits from Auth
Implements the Basic Authentication"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Basic Auth that inherits from auth"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Get encoded part of the authorization header"""
        if authorization_header:
            if type(authorization_header) is str:
                if authorization_header.startswith("Basic "):
                    fields = authorization_header.split(" ")
                    return fields[-1]
        return None
