from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum
from typing import List

class PaymentStatus:
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"

class Status(Enum):
    Success = "Success"
    Failed = "Failed"


# USer schemas
class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserLoginResponse(BaseModel):
    Status : Status
    access_token: str
    token_type: str
# User schema which use to return user withiout password
class UserGlobalSchema(BaseModel):
    email : EmailStr
    username : str
    id : int
    class Config:
        orm_mode = True
        from_attributes = True


class UserResponseSchema(BaseModel):
    email : EmailStr
    username : str
    id : int
    class Config:
        orm_mode = True
        from_attributes = True



class UserResponse(BaseModel):
    Status: Status
    User: UserResponseSchema

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
    date : datetime
    location : str
    latitude : float
    longitude : float
    available_tickets : int
    price_per_ticket : float

    class Config:
        orm_mode = True
        from_attributes = True
    
class EventResponse(BaseModel):
    Status: Status
    Event: EventGlobalSchema

class EventsResponse(BaseModel):
    Status: Status
    Events: List[EventGlobalSchema]


class EventBookResponse(BaseModel):
    Status: Status
    Data : dict

class BookingSchema(BaseModel):
    event_id : int
    user_id : int
    number_of_tickets : int
    total_price : float
    order_status : str
