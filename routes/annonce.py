from fastapi import APIRouter, Request, UploadFile, Depends, HTTPException
from functions.function import remove_dir, upload_image
from models.models import Annonce, Annonce_image
from database.events import Event
from datetime import datetime
from auth.model import User
from auth.events import Event as AuthEvent
from pydantic import HttpUrl, EmailStr


annonce_router = APIRouter(tags=['annonce'])
events = Event()
auth_events = AuthEvent()


@annonce_router.post('/annonce/')
async def add_annonce(request: Request, current_user: User = Depends(auth_events.get_current_user)):
    form_data = await request.form()
    url = form_data.get('url')

    # url validation
    if url != '' and url is not HttpUrl:
        raise HTTPException(status_code=422, detail='url non valide')

    # get datetime
    now = datetime.now()
    date = now.date()
    hour = now.time()

    # upload folder images path
    title = form_data.get('title')
    upload_folder = f'./images/annonces/{title}_{date}_{hour}'

    # creation of the annonce
    annonce_data = {key: value for key,
                    value in form_data.items() if key != "images"}
    annonce = Annonce(**annonce_data, upload_folder=upload_folder)

    # save annonce
    id_annonce = events.add('annonce', annonce)

    images = form_data.getlist("images")
    for image in images:
        file_path = upload_image(upload_folder, image)
        # save image
        annonce_image = Annonce_image(name=file_path, id_annonce=id_annonce)
        events.add('annonce_image', annonce_image)

    return {'id_annonce': id_annonce, **annonce.dict()}


@annonce_router.get('/annonces/')
async def select_all_annonce():
    annonces = events.select_annonce()
    return annonces


@annonce_router.get('/annonces/{id}')
async def find_annonce(id: int):
    annonce = events.find_annonce(id)
    return annonce


@annonce_router.get('/annonce-images/{id}')
async def find_annonce(id: int):
    images = events.find('annonce_image', 'id_annonce', id)
    return images


@annonce_router.delete('/annonces/{id}')
async def delete_annonce(id: int, current_user: User = Depends(auth_events.get_current_user)):

    # get the annonce folder images
    annonce = events.find('annonce', 'id_annonce', id)
    upload_folder = annonce['upload_folder']

    remove_dir(upload_folder)

    events.delete('annonce', 'id_annonce', id)

    return annonce


@annonce_router.put('/annonces/{id}')
async def update_annonce(id: int, annonce: Annonce, current_user: User = Depends(auth_events.get_current_user)):
    
    if annonce.url != '' and annonce.url is not HttpUrl:
        raise HTTPException(status_code=422, detail='url non valide')

    events.update('annonce', 'id_annonce', id, annonce)
    return annonce
