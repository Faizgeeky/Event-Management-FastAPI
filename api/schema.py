from pydantic import BaseModel, EmailStr
from datetime import datetime

# USer schemas
class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

# User schema which use to return user withiout password
class UserGlobalSchema(BaseModel):
    email : EmailStr
    username : str
    id : int
    class Config:
        orm_mode = True
        from_attributes = True

#  Access token schemas 
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user: str
    expiry: float


# Event Schema 
class EventSchema(BaseModel):
    name : str
    date : datetime
    location : str
    available_tickets : int
    price_per_ticket : float


class EventGlobalSchema(BaseModel):
    id : int
    name : str
    date : str
    location : str
    latitude : float
    longitude : float
    available_tickets : int

    
    