from fastapi import UploadFile
import os
import shutil
from datetime import datetime

def upload_image(upload_folder:str, file:UploadFile):
    try:
        # Vérifiez si le dossier d'upload existe, sinon créez-le
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        # Chemin complet du fichier dans le dossier d'upload
        now = datetime.now()
        date = now.date()
        hour = now.time()
        file_path_table = file.filename.split('.')
        file_path_table[0] = file_path_table[0]+'_'+str(date)+'_'+str(hour)
        file_name = '.'.join(file_path_table)
        file_path = os.path.join(upload_folder, file_name)

        # Ouverture du fichier en mode binaire et écriture des données du fichier téléchargé dans le fichier de destination
        with open(file_path, 'wb') as destination_file:
            shutil.copyfileobj(file.file, destination_file)
            
        return file_path
    except Exception as e:
        return {"message": f"Une erreur s'est produite lors du téléchargement du fichier : {str(e)}"}


def remove_file(file_path):
     if os.path.exists(file_path):
        os.remove(file_path)
    
def remove_dir(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)                                                                                                                                                                                                                  