import logging
import time
from http import HTTPStatus

from cassandra.cqlengine import ValidationError
from cassandra.cqlengine.query import DoesNotExist
from CassandraModels import *
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from models import Detail

# from cassandra.cqlengine.models import DoesNotExist

ApiKeyRouter: APIRouter = APIRouter(tags=["API Keys"])
_apiLogger: logging.Logger = logging.getLogger("api")

# Create API Key
@ApiKeyRouter.post(
    path="/key/",
    status_code=HTTPStatus.CREATED,
    summary="Create a API Key",
    responses={
        HTTPStatus.CREATED.value: {
            "description": "201 response is sent on a successful creation of a API Key.",
            "model": Detail,
            "content": {
                "application/json": {
                    "example": {"detail": "b24aj62cb-1625-4ab5-212b-aah08cxc9a"}
                },
            },
        },
    },
)
def createKey():
    key = api_keys.create(creation_epoch=time.time())
    return {"detail": key.key_id}


@ApiKeyRouter.delete(
    path="/key/{key}",
    status_code=HTTPStatus.OK,
    summary="Delete an API Key",
    responses={
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Occurs on a invalid formatted key submitted",
            "model": Detail,
            "content": {
                "application/json": {
                    "example": {"detail": "The key 123-456-789 is not a valid key"}
                },
            },
        },
        HTTPStatus.NOT_FOUND.value: {
            "description": "Occurs if a valid formated key is submitted but does not exist",
            "model": Detail,
            "content": {
                "application/json": {
                    "example": {"detail": "The key 123-456-789 does not exist"}
                },
            },
        },
        HTTPStatus.OK.value: {
            "description": "Occurs on a successful deletion",
            "model": Detail,
            "content": {
                "application/json": {
                    "example": {"detail": "Successfully deleted 123-456-789"}
                },
            },
        },
    },
)
def deleteKey(key: str):
    try:
        _key = api_keys.get(key_id=key)
        api_keys.delete(_key)
    except ValidationError as ex:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail=f"The key {key} is not a valid key",
        )
    except DoesNotExist as e:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail=f"The key {key} does not exist",
        )

    return {"detail": f"Successfully deleted {key}"}
