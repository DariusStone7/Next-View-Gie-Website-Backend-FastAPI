from pydantic import HttpUrl, EmailStr
from fastapi.encoders import jsonable_encoder
from database.connection import Connection
from datetime import datetime

class Event():
    def __init__(self) -> None:
        self.con = Connection.con
        self.cursor = self.con.cursor()

    def add(self, table: str, data: dict):
        """function to add new data in table"""
        try:
            print('\n\nAdding new {}\n\n'.format(table))

            querry = 'INSERT INTO {} VALUES(null'.format(table)
            json_data = jsonable_encoder(data)
            for value in json_data.values():
                if type(value) is str or type(value) is HttpUrl or type(value) is EmailStr:
                    value = value.replace("'", "\\'")
                    querry += ', \'' + str(value) + '\''
                else:
                    querry += ', ' + str(value)
            querry += ');'

            print('querry: ', querry, '\n\n')

            self.cursor.execute(querry)
            self.con.commit()
        except:
            print('Error: falaid to add {}'.format(table))

        inserted_id = self.cursor.lastrowid
        return inserted_id

    def select(self, table: str):
        """function to select data from table"""
        print('\n\nSelect {}\n\n'.format(table))
        try:
            querry = 'SELECT * FROM {};'.format(table)

            print('querry: ', querry, '\n\n')

            # creates a cursor that returns rows as dictionaries
            self.cursor = self.con.cursor(dictionary=True)
            self.cursor.execute(querry)

            result = self.cursor.fetchall()
            data = []
            object = {}
            for row in result:
                for key, value in row.items():
                    object[key] = value
                data.append(row)

            return data
        except:
            print('Error: falaid to select {}'.format(table))


    def selectOrder(self, table: str, attribute: str):
        """function to select data from table"""
        print('\n\nSelect {}\n\n'.format(table))
        try:
            querry = f'SELECT * FROM {table} ORDER BY {attribute};'

            print('querry: ', querry, '\n\n')

            # creates a cursor that returns rows as dictionaries
            self.cursor = self.con.cursor(dictionary=True)
            self.cursor.execute(querry)

            result = self.cursor.fetchall()
            data = []
            object = {}
            for row in result:
                for key, value in row.items():
                    object[key] = value
                data.append(row)

            return data
        except:
            print('Error: falaid to select {}'.format(table))



    def find(self, table: str, attribute: str, value: int | str):
        """function to find any row in table"""
        print('\n\nFind element: {} = {} in table {}\n\n'.format(
            attribute, value, table))
        try:
            querry = 'SELECT * FROM {} WHERE {} = {};'.format(
                table, attribute, value)

            print('querry: ', querry, '\n\n')

            # creates a cursor that returns rows as dictionaries
            self.cursor = self.con.cursor(dictionary=True)
            self.cursor.execute(querry)

            object = {}
            result = self.cursor.fetchone()
            for key, value in result.items():
                object[key] = value

            print(object)
            return object
        except:
            print('Error: falaid to select {}'.format(table))

    def delete(self, table: str, attribute: str, value: int | str):
        """function to delete any row from table"""
        print('\n\nDelete element: {} = {} in table {}\n\n'.format(
            attribute, value, table))
        try:
            querry = 'DELETE FROM {} WHERE {} = {}'.format(
                table, attribute, value)

            print('querry: ', querry, '\n\n')

            self.cursor.execute(querry)
            self.con.commit()
        except:
            print('Error: falaid to delete {}: {} = {}'.format(
                table, attribute, value))

    def update(self, table: str, attibute: str, val: int | str, data: dict):
        """function to update row from table"""
        print('\n\nUpdate table {}: {} = {}\n\n'.format(table, attibute, val))
        try:
            json_data = jsonable_encoder(data)
            # value = type(value) == str ? '\'value\'' : value
            i = 0
            querry = 'UPDATE {} SET '.format(table)
            for key, value in json_data.items():
                if i == 0:
                    if (type(value) == str or type(value) == HttpUrl or type(value) == EmailStr):
                        value = value.replace("'", "\\'")
                        querry += '{} = \'{}\''.format(key, value)
                    else:
                        querry += '{} = {}'.format(key, value)
                    i += 1
                else:
                    if (type(value) == str or type(value) == HttpUrl or type(value) == EmailStr):
                        value = value.replace("'", "\\'")
                        querry += ', {} = \'{}\''.format(key, value)
                    else:
                        querry += ', {} = {}'.format(key, value)
            querry += ' WHERE {} = {};'.format(attibute, val)

            print('querry: ', querry, '\n\n')

            self.cursor.execute(querry)
            self.con.commit()
        except:
            print('Error: Falaid to update table {}'.format(table))

    # fuction to get annonce and the corresponding images
    def select_annonce(self):
        """function to select annonce"""
        print('\n\nSelect annonce whith images\n\n')
        try:
            querry = 'SELECT annonce.id_annonce, annonce.title, annonce.description, annonce.url, annonce.price, annonce.bedroom,annonce.bathroom, annonce.warehouse, annonce.parking, annonce.pool, annonce.wind, annonce.furniture, annonce.fredge, annonce.phone, annonce.address, annonce.email, annonce.upload_folder, GROUP_CONCAT(annonce_image.name) AS images FROM annonce JOIN annonce_image ON annonce.id_annonce=annonce_image.id_annonce GROUP BY annonce.id_annonce;'

            print('querry: ', querry, '\n\n')

            # creates a cursor that returns rows as dictionaries
            self.cursor = self.con.cursor(dictionary=True)
            self.cursor.execute(querry)

            result = self.cursor.fetchall()
            data = []
            object = {}
            for row in result:
                for key, value in row.items():
                    object[key] = value
                data.append(row)
            print(data)

            return data
        except:
            print('Error: falaid to select annonce')

    # fuction to find an annonce and the corresponding images
    def find_annonce(self, id: int):
        """function to select annonce"""
        print('\n\nSelect annonce whith images\n\n')
        try:
            querry = 'SELECT annonce.id_annonce, annonce.title, annonce.description, annonce.url, annonce.price, annonce.bedroom,annonce.bathroom, annonce.warehouse, annonce.parking, annonce.pool, annonce.wind, annonce.furniture, annonce.fredge, annonce.phone, annonce.address, annonce.email, annonce.upload_folder, GROUP_CONCAT(annonce_image.name) AS images, GROUP_CONCAT(annonce_image.id_annonce_image) AS imagesId FROM annonce JOIN annonce_image ON annonce.id_annonce=annonce_image.id_annonce WHERE {}=annonce.id_annonce GROUP BY annonce.id_annonce;'.format(
                id)

            print('querry: ', querry, '\n\n')

            # creates a cursor that returns rows as dictionaries
            self.cursor = self.con.cursor(dictionary=True)
            self.cursor.execute(querry)

            result = self.cursor.fetchall()
            data = []
            object = {}
            for row in result:
                for key, value in row.items():
                    object[key] = value
                data.append(row)
            print(data)

            return data
        except:
            print('Error: falaid to find annonce: id_annonce = {}'.format(id))

    # function to reset user password

    def reset_password(self, username: str, password: str):
        """function to reset user password"""
        print('\n\nReset user password: username = {}\n\n'.format(username))
        try:
            querry = f'UPDATE user SET password = "{password}" WHERE username = "{username}";'

            print('querry: ', querry, '\n\n')

            self.cursor.execute(querry)
            self.con.commit()
        except:
            print(f'Error: Falaid to reset password: username = {username}')

    def make_message_as_read(self, id: int, date: str):
        """function to make message as read"""
        print('\n\Make message as read: id_message = {}\n\n'.format(id))
        try:
            querry = f'UPDATE message SET read_at = "{date}" WHERE id_message = "{id}";'

            print('querry: ', querry, '\n\n')

            self.cursor.execute(querry)
            self.con.commit()
        except:
            print(f'Error: Falaid to make message as read: id_message = {id}')
