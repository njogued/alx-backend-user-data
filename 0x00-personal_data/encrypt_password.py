#!/usr/bin/env python3
"""Implement a hashing password function"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Function to hash a password"""
    password = bytes(password, encoding="utf-8")
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if the hashed password is valid"""
    password = bytes(password, encoding="utf-8")
    return bcrypt.checkpw(password, hashed_password)
