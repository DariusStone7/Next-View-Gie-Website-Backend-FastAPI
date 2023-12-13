from fastapi import APIRouter, Request, Depends
from functions.function import remove_file, upload_image
from models.models import Annonce_image
from database.events import Event
from auth.model import User
from auth.events import Event as AuthEvent

annonce_image_router = APIRouter(tags=['annonce_image'])
events = Event()
auth_events = AuthEvent()

@annonce_image_router.post('/annonce-image/')
async def add_annonce_image(request:Request, current_user: User = Depends(auth_events.get_current_user)):
    form_data = await request.form()
    id_annonce=int(form_data.get("id_annonce"))
    
    #get the annonce folder images
    annonce = events.find('annonce', 'id_annonce', id_annonce)
    upload_folder = annonce['upload_folder']
    
    #upload the image
    file_path = upload_image(upload_folder, form_data.get("image"))
    
    #creation de l'objet annonce_immage
    annonce_image = Annonce_image(name=file_path, id_annonce=id_annonce)
    # annonce_image.image = str(file_path)

    id = events.add('annonce_image', annonce_image)
    
    return {'id_annonce_image': id, **annonce_image.dict()}        

@annonce_image_router.get('/annonces-images/')
async def select_all_annonce_image():
    annonces_images = events.select('annonce_image')
    return annonces_images


@annonce_image_router.get('/annonces-images/{id}')
async def find_annonce_image(id:int):
    annonce_image = events.find('annonce_image', 'id_annonce__image', id)
    return annonce_image


@annonce_image_router.delete('/annonces-images/{id}')
async def delete_annonce_image(id:int, current_user: User = Depends(auth_events.get_current_user)):
    
    result = events.find('annonce_image', 'id_annonce_image', id)
    annonce_image = Annonce_image(**result)
    
    remove_file(annonce_image.name)
    
    events.delete('annonce_image', 'id_annonce_image', id)
    
    return annonce_image


@annonce_image_router.put('/annonces-images/{id}')
async def update_annonce_image(id:int, annonce_image:Annonce_image, current_user: User = Depends(auth_events.get_current_user)):
    events.update('annonce_image', 'id_annonce_image', id, annonce_image)
    return annonce_image