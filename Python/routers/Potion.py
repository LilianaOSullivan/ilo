from fastapi.routing import APIRouter
from fastapi import Form, Request, HTTPException
import Config
from routers.User import userDB

potionRouter = APIRouter()


@potionRouter.post("/potion", include_in_schema=False)
def loggedIn(request: Request, username: str = Form("username")):
    """Returns True or False depending on a users logged in state

    Args:
        username (str): Username to be checked

    Returns:
        bool: True if logged in, False if logged out.
    """
    if not request.client_host == Config.Potion_IP: #Likely needs port appended
        pass
    result = userDB.find_one({"username": username})
    return True
    #return True if result is not None else False