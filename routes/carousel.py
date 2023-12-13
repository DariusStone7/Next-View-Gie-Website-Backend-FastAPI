from fastapi import APIRouter, File, UploadFile, Depends
from models.models import Carousel
from database.events import Event
from functions.function import upload_image, remove_file
from auth.model import User
from auth.events import Event as AuthEvent

carousel_router = APIRouter(tags=['carousel'])
events = Event()
auth_events = AuthEvent()


@carousel_router.post('/carousel/')
async def add_carousel(file: UploadFile = File(...), current_user: User = Depends(auth_events.get_current_user)):
    
    upload_folder = './images/carousels'
    
    #upload the image
    file_path = upload_image(upload_folder, file)
    
    #creation de l'objet carousel
    carousel = Carousel(text='', image='')
    
    #save carousel
    carousel.image = str(file_path)
    
    id = events.add('carousel', carousel)

    return {'id_carousel': id, **carousel.dict()}
   
    
    
@carousel_router.get('/carousels/')
async def select_all_carousel():
    carousels = events.select('carousel')
    return carousels


@carousel_router.get('/carousels/{id}')
async def find_carousel(id:int):
    carousel = events.find('carousel', 'id_carousel', id)
    return carousel


@carousel_router.delete('/carousels/{id}')
async def delete_carousel(id:int, current_user: User = Depends(auth_events.get_current_user)):
    result = events.find('carousel', 'id_carousel', id)
    carousel = Carousel(**result)
    
    remove_file(carousel.image)

    events.delete('carousel', 'id_carousel', id)
    
    return carousel


@carousel_router.put('/carousels/{id}')
async def update_carousel(id:int, carousel:Carousel, current_user: User = Depends(auth_events.get_current_user)):
    events.update('carousel', 'id_carousel', id, carousel)
    return carousel