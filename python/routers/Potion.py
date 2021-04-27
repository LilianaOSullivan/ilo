from CassandraModels import users
from Config import Config
from fastapi import Form, HTTPException, Request
from fastapi.routing import APIRouter
from http import HTTPStatus

potionRouter = APIRouter()


@potionRouter.post("/potion", include_in_schema=False)
def loggedIn(request: Request, address: str = Form("address")):
    """Returns True or False depending on a users logged in state

    Args:
        username (str): Username to be checked

    Returns:
        bool: True if logged in, False if logged out.
    """
    if not request.client.host == Config.Potion_IP:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
    query = users.objects(logged_in=address)
    return True if query.count() > 0 else False
