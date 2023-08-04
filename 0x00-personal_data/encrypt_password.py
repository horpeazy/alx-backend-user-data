#!/usr/bin/env python3
"""encrypt password module"""
import bcrypt
import base64
import hashlib


def hash_password(password: str) -> bytes:
    """hahses a password with a salt
    Parameters
    ----------
    password: str
        password to hash
    """
    hashed = bcrypt.hashpw(
            password.encode(), 
            bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """checks the validity of a password
    Parameters
    ----------
    hashed_password: bytes
        hash of a password
    password: str
        password string
    Returns: bool
    -------
        validity of password
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
