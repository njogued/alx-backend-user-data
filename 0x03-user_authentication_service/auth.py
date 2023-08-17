#!/usr/bin/env python3
"""Methods:
_hash_password: Function to hash password to bytes"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Method to register a new user"""
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(
                email=email, hashed_password=hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Method to check if the user exists and return True or False"""
        try:
            user_obj = self._db.find_user_by(email=email)
            password = password.encode('utf-8')
            return bcrypt.checkpw(password, user_obj.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Find user for given email, generate uuid and return session id"""
        try:
            user_obj = self._db.find_user_by(email=email)
            user_session_id = _generate_uuid()
            self._db.update_user(user_id=user_obj.id,
                                 session_id=user_session_id)
            return user_session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union(User, None):
        """Find user for given session id"""
        if session_id:
            try:
                user_obj = self._db.find_user_by(session_id=session_id)
                return user_obj
            except NoResultFound:
                return None
        return None

    def destroy_session(self, user_id: int) -> None:
        """Method to destroy the user's current session"""
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Get a reset password token if user forgets"""
        try:
            user_obj = self._db.find_user_by(email=email)
            token = uuid4()
            self._db.update_user(user_obj.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Update the password for user with reset token"""
        try:
            user_obj = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user_obj.id, password=hashed_password)
            self._db.update_user(user_obj.id, reset_token=None)
            return None
        except NoResultFound:
            raise ValueError


def _hash_password(password: str) -> bytes:
    """Hashing a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Function to generate and return a string representation of a uuid"""
    return str(uuid4())
