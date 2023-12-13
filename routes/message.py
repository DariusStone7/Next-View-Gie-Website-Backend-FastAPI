from fastapi import APIRouter, Body, Depends
from models.models import Message
from database.events import Event
from auth.model import User
from auth.events import Event as AuthEvent


message_router = APIRouter(tags=['message'])
events = Event()
auth_events = AuthEvent()


@message_router.post('/message/')
async def add_message(message:Message, current_user: User = Depends(auth_events.get_current_user)):
    id = events.add('message', message)
    return {'id_message': id, **message.dict()}
        

@message_router.get('/messages/')
async def select_all_message():
    messages = events.selectOrder('message', 'read_at')
    return messages


@message_router.get('/messages/{id}')
async def find_message(id:int):
    message = events.find('message', 'id_message', id)
    return message


@message_router.delete('/messages/{id}')
async def delete_message(id:int, current_user: User = Depends(auth_events.get_current_user)):
    events.delete('message', 'id_message', id)
    return {'id_message':id}

@message_router.put('/messages/{id}')
async def update_message(id:int, message:Message, current_user: User = Depends(auth_events.get_current_user)):
    events.update('message', 'id_message', id, message)
    return message      


@message_router.put('/message-read/{id}')
async def update_message(id:int, date:str= Body(), current_user: User = Depends(auth_events.get_current_user)):
    events.make_message_as_read(id, date)
    return {'date': date}