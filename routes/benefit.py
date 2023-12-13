from fastapi import APIRouter, Depends
from models.models import Benefit
from database.events import Event
from auth.model import User
from auth.events import Event as AuthEvent

benefit_router = APIRouter(tags=['benefit'])
events = Event()
auth_events = AuthEvent()


@benefit_router.post('/benefit/')
async def add_benefit(benefit:Benefit, current_user: User = Depends(auth_events.get_current_user)):
    id = events.add('benefit', benefit)
    
    return {'id_benefit': id, **benefit.dict()}
        

@benefit_router.get('/benefits/')
async def select_all_benefit():
    benefits = events.select('benefit')
    return benefits


@benefit_router.get('/benefits/{id}')
async def find_benefit(id:int):
    benefit = events.find('benefit', 'id_benefit', id)
    return benefit


@benefit_router.delete('/benefits/{id}')
async def delete_benefit(id:int, current_user: User = Depends(auth_events.get_current_user)):
    events.delete('benefit', 'id_benefit', id)


@benefit_router.put('/benefits/{id}')
async def update_benefit(id:int, benefit:Benefit, current_user: User = Depends(auth_events.get_current_user)):
    events.update('benefit', 'id_benefit', id, benefit)
    return benefit