from fastapi import APIRouter, Depends
from models.models import Service_technology
from database.events import Event
from auth.model import User
from auth.events import Event as AuthEvent


service_technology_router = APIRouter(tags=['service-technology'])
events = Event()
auth_events = AuthEvent()


@service_technology_router.post('/service-technology/')
async def add_service_technology(service_technology:Service_technology, current_user: User = Depends(auth_events.get_current_user)):
    id = events.add('service_technology', service_technology)
    return {'id_service_technology': id, **service_technology.dict()}
        

@service_technology_router.get('/service-technology/')
async def select_all_service_technology():
    service_technologys = events.select('service_technology')
    return service_technologys


@service_technology_router.get('/service-technology/{id}')
async def find_service_technology(id:int):
    service_technology = events.find('service_technology', 'id_service_technology', id)
    return service_technology


@service_technology_router.delete('/service-technology/{id}')
async def delete_service_technology(id:int, current_user: User = Depends(auth_events.get_current_user)):
    events.delete('service_technology', 'id_service_technology', id)


@service_technology_router.put('/service-technology/{id}')
async def update_service_technology(id:int, service_technology:Service_technology, current_user: User = Depends(auth_events.get_current_user)):
    events.update('service_technology', 'id_service_technology', id, service_technology)
    return service_technology