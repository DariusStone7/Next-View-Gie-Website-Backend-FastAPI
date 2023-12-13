from fastapi import APIRouter,Depends
from models.models import Service_benefit
from database.events import Event
from auth.model import User
from auth.events import Event as AuthEvent

service_benefit_router = APIRouter(tags=['service-benefit'])
events = Event()
auth_events = AuthEvent()

@service_benefit_router.post('/service-benefit/')
async def add_service_benefit(service_benefit:Service_benefit, current_user: User = Depends(auth_events.get_current_user)):
    id = events.add('service_benefit', service_benefit)
    return {'id_service_benefit': id, **service_benefit.dict()}
        

@service_benefit_router.get('/service-benefit/')
async def select_all_service_benefit():
    service_benefits = events.select('service_benefit')
    return service_benefits


@service_benefit_router.get('/service-benefit/{id}')
async def find_service_benefit(id:int):
    service_benefit = events.find('service_benefit', 'id_service_benefit', id)
    return service_benefit


@service_benefit_router.delete('/service-benefit/{id}')
async def delete_service_benefit(id:int, current_user: User = Depends(auth_events.get_current_user)):
    events.delete('service_benefit', 'id_service_benefit', id)


@service_benefit_router.put('/service-benefit/{id}')
async def update_service_benefit(id:int, service_benefit:Service_benefit, current_user: User = Depends(auth_events.get_current_user)):
    events.update('service_benefit', 'id_service_benefit', id, service_benefit)
    return service_benefit