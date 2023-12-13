from fastapi import APIRouter, Request, Depends
from functions.function import remove_file, upload_image
from models.models import Member_profile
from database.events import Event
from auth.model import User
from auth.events import Event as AuthEvent


member_profile_router = APIRouter(tags=['member-profile'])
events = Event()
auth_events = AuthEvent()


@member_profile_router.post('/member-profile/')
async def add_member_profile(request:Request, current_user: User = Depends(auth_events.get_current_user)):
   form_data = await request.form()

   upload_folder = './images/members'
    
   file_path = upload_image(upload_folder, form_data.get("image"))

   #creation de l'objet service
   profile_data = {**form_data, "image": file_path} #créer un nouveau dictionnaire et remplace la valeur de la cle image par file_path
   profile = Member_profile(**profile_data)

   # save service
   id = events.add('member_profile', profile)

   return {'id_member_profile': id, **profile.dict()}


@member_profile_router.get('/members-profiles/')
async def select_all_member_profile():
    member_profiles = events.select('member_profile')
    return member_profiles


@member_profile_router.get('/members_profiles/{id}')
async def find_member_profile(id:int):
    member_profile = events.find('member_profile', 'id_member_profile', id)
    return member_profile


@member_profile_router.delete('/members-profiles/{id}')
async def delete_member_Profile(id:int, current_user: User = Depends(auth_events.get_current_user)):
    
    result = events.find('member_profile', 'id_member_profile', id)
    profile = Member_profile(**result)
    
    remove_file(profile.image)
    
    events.delete('member_profile', 'id_member_profile', id)
    return profile


@member_profile_router.put('/members-profiles/{id}')
async def update_member_profile(id:int, request:Request, current_user: User = Depends(auth_events.get_current_user)):
    form_data = await request.form()

    upload_folder = './images/members'
    
    if(type(form_data.get("image")) != str):
        remove_file(form_data.get("oldImage"))
        file_path = upload_image(upload_folder, form_data.get("image"))
        member_data = {**form_data, "image": file_path} #créer un nouveau dictionnaire et remplace la valeur de la cle image par file_path
    else:
        member_data = {**form_data} 
        
    #creation de l'objet member
    member_profile = Member_profile(**member_data)
    
    # update member
    events.update('member_profile', 'id_member_profile', id, member_profile)
     
    return member_profile