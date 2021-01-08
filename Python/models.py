from typing import Optional, Union

from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: Union[str, bytes]
    public_key: Optional[str] = None
    logged_in: Optional[bool] = None

    apiKey: Optional[str] = None


class Detail(BaseModel):
    detail: str = ""
