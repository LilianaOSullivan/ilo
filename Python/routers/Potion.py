from fastapi.routing import APIRouter
from fastapi import Form

potionRouter = APIRouter()


@potionRouter.post("/potion", include_in_schema=False)
def loggedIn(username: str = Form("username")):
    print(username)
    return True
