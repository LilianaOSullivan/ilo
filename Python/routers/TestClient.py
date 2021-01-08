from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter

TestClient: APIRouter = APIRouter(
    default_response_class=HTMLResponse, tags=["Test Client"]
)


@TestClient.get(path="/")
def home():
    with open("client/login.html") as f:
        return f.read()


@TestClient.get(path="/message")
def home():
    with open("client/sendMessage.html") as f:
        return f.read()


@TestClient.get(
    path="/client/static/socket_code.js",
    include_in_schema=False,
)
def jsFile():
    with open("client/static/socket_code.js") as f:
        return f.read()
