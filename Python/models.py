from typing import Optional, Union

from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: Union[str, bytes]
    public_key: str
    api_key: str


class Detail(BaseModel):
    detail: str = ""
