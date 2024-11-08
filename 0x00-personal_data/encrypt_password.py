#!/usr/bin/env python3

"""Module for encrypting passwords."""

import logging
import bcrypt

def generate_password_hash(input_password: str) -> bytes:
    """
    Hashes the provided password using bcrypt.

    Args:
        input_password (str): Password to be hashed.

    Returns:
        bytes: A salted, hashed password in byte string format.
    """
    # Salt and hash the password using the bcrypt package
    return bcrypt.hashpw(input_password.encode('utf-8'), bcrypt.gensalt())

def verify_password(hashed_credentials: bytes, provided_password: str) -> bool:
    """
    Validates that the provided password matches the hashed password.

    Args:
        hashed_credentials (bytes): Hashed password.
        provided_password (str): Password to be validated.

    Returns:
        bool: True if the hashed password was formed from the given password, otherwise False.
    """
    try:
        # Attempt to match the hashed password with the given password
        return bcrypt.checkpw(provided_password.encode('utf-8'), hashed_credentials)
    except Exception as error:
        # Log any exceptions during password validation
        logging.error("Password validation error: {}".format(error))
        return False