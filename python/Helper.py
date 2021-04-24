import logging
import re

from CassandraModels import api_keys

logger: logging.Logger = None


def validate_APIKey(
    key: str,
) -> bool:
    """
    Checks if an API Key is valid. Returns False if it's empty

    Parameters:
            key (str): The key to be validated

    Returns:
            bool: True if the key is valid, False if its invalid or empty.
    """
    if not (key := key.strip()):
        return False
    query = api_keys.objects(key_id=key)
    return False if query.count() == 0 else True


def validate_password(password: str) -> bool:
    """
    Validates that a password is meeting the minimum criteria, with confirmation.
    It must at minimum
        - Be of length 8
        - Contain minimum 1 number
        - Contain minimum 1 lowercase letter
        - Contain minimum 1 uppercase letter
        - 1 non-alphanumeric character

    Args:
        password (str): The password to validate

    Returns:
        bool: True if valid, False if invalid
    """
    if len(password) < 8:
        return False
    if re.search("[0-9]+", password) == None:  # Number
        return False
    if re.search("[a-z]+", password) == None:  # Lowercase
        return False
    if re.search("[A-Z]+", password) == None:  # Uppercase
        return False
    if re.search("[^\w\d\s]+", password) == None:  # Special character
        return False
    return True
