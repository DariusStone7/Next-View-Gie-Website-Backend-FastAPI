from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    password: str
    image: str
    name: str

class UserOut(BaseModel):
    username: str
    email: str | None = None
    image: str
    name: str
