import json
from pydantic import BaseModel, EmailStr, HttpUrl, Field
from typing import Optional, List, Union
from fastapi import File, UploadFile

class About(BaseModel):
    title : str
    text : str
    image : str
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class Annonce(BaseModel):
    title : str
    description : str
    url : Union[None, str]
    price : int
    bedroom : int = Field(default=0)
    bathroom : bool = Field(default=True)
    warehouse : bool = Field(default=False)
    parking : bool = Field(default=True)
    pool : bool = Field(default=False)
    wind : bool = Field(default=True)
    furniture : bool = Field(default=True)
    fredge : bool = Field(default=True)
    phone : str = Field(default='+237 698 154 430')
    address : str
    email : EmailStr = Field(default='info@next-view.com')
    upload_folder: str


class Annonce_image(BaseModel):
    name : str
    id_annonce : int


class Benefit(BaseModel):
    title : str
    description : str


class Carousel(BaseModel):
    text : Union[None, str]
    image : str


class Customer_feedback(BaseModel):
    name : str
    role : str
    message : str
    image : str
    
class Member_profile(BaseModel):
    name : str
    role : str
    image : str


class Message(BaseModel):
    name : str
    email : str
    phone : str = Field(min_length=9, max_length=13)
    subject : str
    text : str
    create_at: str
    read_at: str


class Service(BaseModel):
    title : str
    description : str
    image : str
    icon : str

class Setting(BaseModel):
    phone: str
    email: str
    facebook: str
    twitter: str    
    linkedin: str
    youtube: str

class Service_benefit(BaseModel):
    title : str
    description : str


class Service_technology(BaseModel):
    title : str
    description : str




    
    

