import logging
import time
import uuid
from http import HTTPStatus
from typing import Dict

from Config import Config
import pymongo
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from models import Detail
from pymongo.collection import Collection


ApiKeyRouter: APIRouter = APIRouter(tags=["API Keys"])
_apiLogger: logging.Logger = logging.getLogger("api")

_keyDB: Collection = pymongo.MongoClient(Config.MongoDB_address)[
    Config.MongoDB_database
][Config.MongoDB_apiKey_collection]

# Create API Key
@ApiKeyRouter.post(
    path="/key/", status_code=HTTPStatus.CREATED, summary="Create a API Key"
)
def createKey():
    key: str = str(uuid.uuid1())
    _keyDB.insert_one(
        {
            "key": key,
            "lastUpdated": time.time(),
        }
    )
    return {"detail": key}


@ApiKeyRouter.delete(
    path="/key/{key}",
    status_code=HTTPStatus.OK,
    summary="Delete an API Key",
    responses={  # BUG: This needs to completed, just copied and pasted from previous method.
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Occurs on a invalid key submitted",
            "model": Detail,
            "content": {
                "application/json": {
                    "example": {"detail": "The API Key 123-456-789 does not exist"}
                },
            },
        },
    },
)
def deleteKey(key: str):
    x = _keyDB.find_one_and_delete({"key": key})
    if x is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"The API Key {key} does not exist",
        )
    return {"detail": f"Successfully deleted {key}"}


def fnd_int():
    pass
