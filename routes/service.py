from fastapi import APIRouter, Request, Depends
from models.models import Service
from database.events import Event
from functions.function import upload_image, remove_file, remove_dir
from auth.model import User
from auth.events import Event as AuthEvent


service_router = APIRouter(tags=['service'])
events = Event()
auth_events = AuthEvent()


@service_router.post('/service/')
async def add_service(request:Request, current_user: User = Depends(auth_events.get_current_user)):
    
    form_data = await request.form()

    upload_folder = './images/services'
    
    file_path = upload_image(upload_folder, form_data.get("image"))

    #creation de l'objet service
    service_data = {**form_data, "image": file_path} #créer un nouveau dictionnaire et remplace la valeur de la cle image par file_path
    service = Service(**service_data)
    
    # save service
    id = events.add('service', service)
    
    return {'id_service': id, **service.dict()}
        

@service_router.get('/services/')
async def select_all_service():
    services = events.select('service')
    return services


@service_router.get('/services/{id}')
async def find_service(id:int):
    service = events.find('service', 'id_service', id)
    return service


@service_router.delete('/services/{id}')
async def delete_service(id:int, current_user: User = Depends(auth_events.get_current_user)):
    result = events.find('service', 'id_service', id)
    service = Service(**result)
    
    remove_file(service.image)
    
    events.delete('service', 'id_service', id)

    return service

    
@service_router.put('/services/{id}')
async def update_service(id:int, request:Request, current_user: User = Depends(auth_events.get_current_user)):
    form_data = await request.form()

    upload_folder = './images/services'
    
    if(type(form_data.get("image")) != str):
        remove_file(form_data.get("oldImage"))
        file_path = upload_image(upload_folder, form_data.get("image"))
        service_data = {**form_data, "image": file_path} #créer un nouveau dictionnaire et remplace la valeur de la cle image par file_path
    else:
        service_data = {**form_data} 
        
    #creation de l'objet service
    service = Service(**service_data)
    
    # update service
    events.update('service', 'id_service', id, service)
    
    return service
    