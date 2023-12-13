import os
from fastapi import HTTPException, Depends, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from passlib.context import CryptContext
from database.events import Event
from auth.model import User, TokenData, Token, UserOut
from jose import jwt, JWTError
from typing import Annotated
from time import time

event = Event()


class Event:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

    def __int__(self) -> None:
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def verify_password(self, plain_password, hashed_password):
        return CryptContext(schemes=['bcrypt'], deprecated='auto').verify(plain_password, hash=hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def add_user(self, user: User):
        user.password = CryptContext(
            schemes=['bcrypt'], deprecated='auto').hash(user.password)
        id = event.add('user', user)
        return {**user.dict()}

    @staticmethod
    def get_user(username: str):
        users = event.select('user')
        for user in users:
            if user['username'] == username or user['email'] == username:
                return User(**user)

    def authenticate_user(self, username: str, password: str):
        user = Event.get_user(username)
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False
        return user

    def create_access_token(self, data: dict, expire_delta: timedelta | None = None):
        to_encode = data.copy()
        if expire_delta:
            expire = datetime.utcnow() + expire_delta
        else:
            expire = datetime.utcnow() + expire_delta(minutes=100)
        to_encode.update({'exp': expire})
        encode_jwt = jwt.encode(to_encode, os.getenv(
            'SECRET_KEY'), algorithm=os.getenv("ALGORITHM"))
        return encode_jwt

    async def get_current_user(self, token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl='token'))]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not available credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        try:
            payload = jwt.decode(token, os.getenv(
                'SECRET_KEY'), algorithms=os.getenv('ALGORITHM'))
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except:
            raise credentials_exception
        user = self.get_user(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    @staticmethod
    def delete_user(username: str):
        username_value = '"' + username + '"'
        event.delete('user', 'username', username_value)

    @staticmethod
    def select_users():
        return event.select('user')

    @staticmethod
    def update_user(table: str, attibute: str, val: int | str, data: dict):
        return event.update(table, attibute, val, data)

    @staticmethod
    def reset_user_password(username: str, password: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Could not available credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        user = Event.get_user(username)
        if not user:
            raise credentials_exception
        password = CryptContext(
            schemes=['bcrypt'], deprecated='auto').hash(password)
        return event.reset_password(username, password)
