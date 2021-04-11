import logging
import time
from http import HTTPStatus


from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from models import Detail
from CassandraModels import *

ApiKeyRouter: APIRouter = APIRouter(tags=["API Keys"])
_apiLogger: logging.Logger = logging.getLogger("api")

# Create API Key
@ApiKeyRouter.post(
    path="/key/", status_code=HTTPStatus.CREATED, summary="Create a API Key"
)
def createKey():
    key = api_keys.create(creation_epoch = time.time())
    return {"detail": key.key_id}


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
    breakpoint()
    api_keys.delete(api_keys.get(key_id=key))
    return {"detail": f"Successfully deleted {key}"}