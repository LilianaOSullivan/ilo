from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    public_key: str
    api_key: str


class Detail(BaseModel):
    detail: str = ""
