#!/usr/bin/env python3
"""A BASICAUTH class that inherits from Auth
Implements the Basic Authentication"""
from api.v1.auth.auth import Auth
import base64


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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """Decode the base64 auth string in header"""
        decoded = None
        if base64_authorization_header:
            if type(base64_authorization_header) is str:
                try:
                    decoded = base64.b64decode(base64_authorization_header)
                    decoded = decoded.decode()
                except:
                    pass
        return decoded
