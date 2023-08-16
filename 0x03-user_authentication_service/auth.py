#!/usr/bin/env python3
"""Methods:
_hash_password: Function to hash password to bytes"""
import bcrypt
from db import DB
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Method to register a new user"""
        if (self._db.find_user_by(email=email)):
            raise ValueError(f"User {email} already exists")
        else:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(
                email=email, hashed_password=hashed_password)
        return new_user


def _hash_password(password: str) -> bytes:
    """Hashing a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
