from fastapi import APIRouter, File, UploadFile, Request, Depends
from models.models import About
from database.events import Event
from auth.events import Event as AuthEvent
from functions.function import upload_image, remove_file
from auth.model import User

about_router = APIRouter(tags=['about'])
events = Event()
auth_events = AuthEvent()


@about_router.post("/about/")
async def add_about(request: Request, current_user: User = Depends(auth_events.get_current_user)):
    
    form_data = await request.form()
    
    upload_folder = './images/about'
    
    file_path = upload_image(upload_folder, form_data.get("image"))

    #creation de l'objet about
    about_data = {**form_data, "image": file_path} #créer un nouveau dictionnaire et remplace la valeur de la cle image par file_path
    about = About(**about_data)
    
    #save about
    id = events.add('about', about)
    
    return {'id_about': id, **about.dict()}
    
        

@about_router.get('/abouts/')
# async def select_all_about( current_user: User = Depends(auth_events.get_current_user)):
async def select_all_about():

    abouts = events.select('about')
    return abouts


@about_router.get('/abouts/{id}')
async def find_about(id:int):
    about = events.find('about', 'id_about', id)
    return about


@about_router.delete('/abouts/{id}')
async def delete_about(id:int, current_user: User = Depends(auth_events.get_current_user)):
    result = events.find('about', 'id_about', id)
    about = About(**result)
    
    remove_file(about.image)
    
    events.delete('about', 'id_about', id)

    return about


@about_router.put('/abouts/{id}')
async def update_about(id:int,request: Request, current_user: User = Depends(auth_events.get_current_user)):
     form_data = await request.form()

     upload_folder = './images/about'
    
     if(type(form_data.get("image")) != str):
         remove_file(form_data.get("oldImage"))
         file_path = upload_image(upload_folder, form_data.get("image"))
         about_data = {**form_data, "image": file_path} #créer un nouveau dictionnaire et remplace la valeur de la cle image par file_path
     else:
         about_data = {**form_data} 
        
     #creation de l'objet service
     about = About(**about_data)
    
     # update about
     events.update('about', 'id_about', id, about)
     
     return about