import logging

from pymongo.collection import Collection


logger: logging.Logger = None
keyDB: Collection = None


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

    key = keyDB.find_one({"key": key})
    return False if key is None else True
