from pydantic import BaseModel
from typing import Union

class Item(BaseModel):
    name: str

class ItemNumber(BaseModel):
    number: int

class Resources(BaseModel):
    res: list[str]

class Urls(BaseModel):
    urls: list[str]

class UserSchema(BaseModel):
    email: str
    password: str

class TokenPayload(BaseModel):
    sub: Union[str, None] = None
    exp: Union[int, None] = None

class SystemUser(BaseModel):
    id: int
    email: str
    is_active: bool = True
    is_superuser: bool = False
