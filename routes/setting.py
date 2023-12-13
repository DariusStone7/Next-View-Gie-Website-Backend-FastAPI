from fastapi import APIRouter, Request, Depends
from models.models import Setting
from database.events import Event
from functions.function import upload_image, remove_file, remove_dir
from auth.model import User
from auth.events import Event as AuthEvent


setting_router = APIRouter(tags=['setting'])
events = Event()
auth_events = AuthEvent()


@setting_router.post('/setting/')
async def add_setting(request:Request, current_user: User = Depends(auth_events.get_current_user)):
    
    form_data = await request.form()

    #creation de l'objet setting
    setting_data = {**form_data} #créer un nouveau dictionnaire et remplace la valeur de la cle image par file_path
    setting = Setting(**setting_data)
    
    # save setting
    id = events.add('setting', setting)
    
    return {'id_setting': id, **setting.dict()}
        

@setting_router.get('/settings/')
async def select_all_settings():
    settings = events.select('setting')
    return settings


@setting_router.get('/settings/{id}')
async def find_setting(id:int):
    setting = events.find('setting', 'id_setting', id)
    return setting


@setting_router.delete('/settings/{id}')
async def delete_setting(id:int, current_user: User = Depends(auth_events.get_current_user)):
    result = events.find('setting', 'id_setting', id)
    setting = Setting(**result)
    
    events.delete('setting', 'id_setting', id)

    return setting

    
@setting_router.put('/settings/{id}')
async def update_setting(id:int, request:Request, current_user: User = Depends(auth_events.get_current_user)):
    form_data = await request.form()

    setting_data = {**form_data} 
        
    #creation de l'objet setting
    setting = Setting(**setting_data)
    
    # update service
    events.update('setting', 'id_setting', id, setting)
    
    return setting
    