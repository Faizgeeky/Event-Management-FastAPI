from pydantic import BaseModel, EmailStr


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