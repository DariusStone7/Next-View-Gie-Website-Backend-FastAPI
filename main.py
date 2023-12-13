from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from mysql.connector import Error
from database.connection import Connection
from routes.about import about_router
from routes.annonce import annonce_router
from routes.annonce_image import annonce_image_router
from routes.benefit import benefit_router
from routes.carousel import carousel_router
from routes.customer_feedback import customer_feedback_router
from routes.member_profile import member_profile_router
from routes.message import message_router
from routes.setting import setting_router
from routes.service import service_router
from routes.service_benefit import service_benefit_router
from routes.service_technology import service_technology_router
from auth.routes import user_router

app = FastAPI(title='Next-View GIE API', version='1.0')


# Configuration du middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Verification of the connection to mysql database
@app.on_event('startup')
async def on_startup():
    con = Connection.con
    cursor = con.cursor()
    try:
        print('\n\n\n************************************** Connection status *****************************')
        if  con.is_connected():
            db_info =  con.get_server_info()
            print('Connected to MySQL server version', db_info)
            cursor.execute('select database();')
            record = cursor.fetchone()
            print('Connected to database:', record, '\n\n')
    except Error as e:
        print('Error while connection to MySQL \n\n', e)


#add routes
app.include_router(about_router)
app.include_router(annonce_router)
app.include_router(annonce_image_router)
app.include_router(benefit_router)
app.include_router(carousel_router)
app.include_router(customer_feedback_router)
app.include_router(member_profile_router)
app.include_router(message_router)
app.include_router(setting_router)
app.include_router(service_router)
app.include_router(service_benefit_router)
app.include_router(service_technology_router)
app.include_router(user_router)

# Montage du dossier "images" pour servir les fichiers statiques
app.mount("/images", StaticFiles(directory="images"), name="image")

if __name__ == '__main__':
    uvicorn.run(app=app, host='127.0.0.1', port=8000)