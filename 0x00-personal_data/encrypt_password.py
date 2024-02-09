#!/usr/bin/env python3
# File: encrypt_password.py
# Author: Oluwatobiloba Light
"""Hash a password"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a salted, hashed password, which is a byte string."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validate that the provided password matches the hashed password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
