import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from jose import jwt, JWTError

load_dotenv(dotenv_path='.env')


class Connection:
    con = mysql.connector.connect(
                host=os.getenv("HOST"),
                database=os.getenv("DBNAME"),
                user=os.getenv("USER"),
                password=os.getenv("PASSWORD")
            )
    def __init__(self):
        try:
            if  Connection.con.is_connected():
                db_info =  Connection.con.get_server_info()
                print('Connected to MySQL server version', db_info)
                cursor =  Connection.con.cursor()
                cursor.execute('select database();')
                record = cursor.fetchone()
                print('Connected to database: ', record)
        except Error as e:
            print('Error while connection to MySQL', e)




