#!/usr/bin/env python3
"""Implement a hashing password function"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Function to hash a password"""
    password = b"{password}"
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_password
