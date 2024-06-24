from pydantic import BaseModel
from typing import Union, List

class Item(BaseModel):
    name: str

class ItemNumber(BaseModel):
    number: int

class UserSchema(BaseModel):
    email: str
    password: str

class PostSchema(BaseModel):
    post_id: int
    post: str
    url: str
    title: str

class TokenPayload(BaseModel):
    sub: Union[str, None] = None
    exp: Union[int, None] = None

class SystemUser(BaseModel):
    id: int
    email: str

class PostRequest(BaseModel):
    user_id: int
    content: str

class ParseTitlesRequest(BaseModel):
    resources: List[str]
    urls: List[str]
    period_days: int

class ProgressRequest(BaseModel):
    user_id: int
    status: str

class ParseArticleRequest(BaseModel):
    url: str