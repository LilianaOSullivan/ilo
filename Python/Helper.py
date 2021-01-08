import logging
from pymongo.collection import Collection



class Helper:
    logger: logging.Logger = None
    keyDB: Collection = None

    @staticmethod
    def validate_APIKey(
        self, key: str
    ) -> bool:  ## QUESTION: Should types be checked? Eg isinstance(key,str)
        """
        Checks if an API Key is valid. Returns False if it's empty

        Parameters:
                key (str): The key to be validated

        Returns:
                bool: True if the key is valid, False if its invalid or empty.
        """
        if not (key := key.strip()):
            return False

        key = self.keyDB.find_one({"key": key})
        return False if key is None else True