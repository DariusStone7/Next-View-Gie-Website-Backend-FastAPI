from fastapi import APIRouter, Request, Depends
from functions.function import remove_file, upload_image
from models.models import Customer_feedback
from database.events import Event
from auth.model import User
from auth.events import Event as AuthEvent


customer_feedback_router = APIRouter(tags=['customer_feedback'])
events = Event()
auth_events = AuthEvent()


@customer_feedback_router.post('/customer-feedback/')
async def add_customer_feedback(request:Request, current_user: User = Depends(auth_events.get_current_user)):
   form_data = await request.form()

   upload_folder = './images/feedbacks'
    
   file_path = upload_image(upload_folder, form_data.get("image"))

   #creation de l'objet feedback
   feedback_data = {**form_data, "image": file_path} #créer un nouveau dictionnaire et remplace la valeur de la cle image par file_path
   feedback = Customer_feedback(**feedback_data)
    
   # save feedback
   id = events.add('customer_feedback', feedback)
    
   return {'id_customer_feedback': id, **feedback.dict()}
        

@customer_feedback_router.get('/customers-feedbacks/')
async def select_all_customer_feedback():
    customer_feedbacks = events.select('customer_feedback')
    return customer_feedbacks


@customer_feedback_router.get('/customers-feedbacks/{id}')
async def find_customer_feedback(id:int):
    customer_feedback = events.find('customer_feedback', 'id_customer_feedback', id)
    return customer_feedback


@customer_feedback_router.delete('/customers-feedbacks/{id}')
async def delete_customer_feedback(id:int, current_user: User = Depends(auth_events.get_current_user)):
    result = events.find('customer_feedback', 'id_customer_feedback', id)
    feedback = Customer_feedback(**result)
    
    remove_file(feedback.image)
    events.delete('customer_feedback', 'id_customer_feedback', id)

    return feedback


@customer_feedback_router.put('/customers-feedbacks/{id}')
async def update_customer_feedback(id:int, request:Request, current_user: User = Depends(auth_events.get_current_user)):
    form_data = await request.form()

    upload_folder = './images/feedbacks'
    
    if(type(form_data.get("image")) != str):
        remove_file(form_data.get("oldImage"))
        file_path = upload_image(upload_folder, form_data.get("image"))
        feedback_data = {**form_data, "image": file_path} #créer un nouveau dictionnaire et remplace la valeur de la cle image par file_path
    else:
        feedback_data = {**form_data} 
        
    #creation de l'objet feedback
    customer_feedback = Customer_feedback(**feedback_data)
    
    # update feedback
    events.update('customer_feedback', 'id_customer_feedback', id, customer_feedback)

    return customer_feedback