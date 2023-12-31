#!/usr/bin/env python3
"""A BASICAUTH class that inherits from Auth
Implements the Basic Authentication"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


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
                except Exception:
                    pass
        return decoded

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """Return user credentials in decodebase64 authorization"""
        if decoded_base64_authorization_header:
            if type(decoded_base64_authorization_header) is str:
                if ':' in decoded_base64_authorization_header:
                    cred_list = decoded_base64_authorization_header.split(':')
                    creds = (cred_list[0], cred_list[1])
                    return creds
        return (None, None)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Return the user object from creds"""
        email_dict = {}
        email_dict['email'] = user_email
        if user_email is None or user_pwd is None or type(user_email)\
                is None or type(user_pwd) is None:
            return None
        try:
            user = User.search(email_dict)
            if user is None or user == []:
                return None
            else:
                for one_user in user:
                    if one_user.is_valid_password(user_pwd):
                        return one_user
                return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """method  that overloads Auth
        and retrieves the User instance for a request:
        """
        auth_header = self.authorization_header(request)
        if auth_header is not None:
            token = self.extract_base64_authorization_header(auth_header)
            if token is not None:
                decoded = self.decode_base64_authorization_header(token)
                if decoded is not None:
                    email, password = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(
                            email, password)
        return
