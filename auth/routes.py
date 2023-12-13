from fastapi import APIRouter, Request, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth.model import User, Token, UserOut
from auth.events import Event
from typing import Annotated
from datetime import datetime, timedelta
from functions.function import upload_image, remove_file


user_router = APIRouter(tags=['user'])
events = Event()

@user_router.post('/user', response_model=User)
async def add_user(user: Annotated[User, Depends(events.get_current_user)]):
    return events.add_user(user)


@user_router.post('/token')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = events.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={"WWW-Authentificate": "Bearer"},
        )
    access_token_expire = timedelta(days=1)
    access_token = events.create_access_token(
        data={"sub": user.username}, expire_delta=access_token_expire
    )
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.get("/users/me/", response_model=UserOut)
async def get_current_user(current_user: Annotated[User, Depends(events.get_current_user)]):
    return current_user


@user_router.get("/users/")
async def select_users():
    return events.select_users()


@user_router.delete("/users/{username}")
async def delete_user(username: str, current_user: Annotated[User, Depends(events.get_current_user)]):
    return events.delete_user(username)


@user_router.put("/user/{username}")
async def update_user(username: str, request:Request, current_user: User = Depends(events.get_current_user)):
    form_data = await request.form()

    upload_folder = './images/adminProfile'
    
    if(type(form_data.get("image")) != str):
        remove_file(form_data.get("oldImage"))
        file_path = upload_image(upload_folder, form_data.get("image"))
        user_data = {**form_data, "image": file_path} #créer un nouveau dictionnaire et remplace la valeur de la cle image par file_path
    else:
        user_data = {**form_data} 
        
    #creation de l'objet user
    user = UserOut(**user_data)
    
    # update about
    events.update_user('user', 'username', f'"{username}"', user)
     
    return user

@user_router.put('/user-password/{username}')
async def reset_password(username: str, password: str = Body()):
    events.reset_user_password(username, password)
