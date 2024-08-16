from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError
from api.models import Users
from api.schema import UserSchema, UserLoginSchema, TokenData, UserGlobalSchema, UserLoginResponse, Status, UserResponse, UserResponseSchema
from api.database import get_db
import jwt
import api.config as config
import time
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(tags=["User Authentication"])

def create_access_token(data: dict):
    # set up the expiry time for this token to custom from ENV variable
    expire = time.time() + config.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    payload = {
        "user":data['user'],
        "expiry" : expire
    }
    # encode the payload data use user related data like - id , email - unique data is recommended
    encoded_jwt = jwt.encode(payload, config.JWT_SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt

# NOTE : This can be enhanced logout blacklist token adding refresh token
def verify_token(token: str):
    try:
        # decode the token with secreate key and check the expiry time
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.ALGORITHM])
        print("data us ", payload , type(payload.get('expiry')) , type(time.time()))
        if payload.get("expiry") >= time.time():
            print("reached here")
            return TokenData(user=payload.get("user"), expiry=payload.get("expiry"))
        else:
            raise HTTPException(status_code=401, detail="Token has expired")

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# It allows to read beare token from swagger ui
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not verify_token(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")


@router.post('/auth/register', summary="Add new user", response_model=UserResponse)
def register(request : UserSchema, db: Session = Depends(get_db)):
    try:
        user = Users(username = request.username,email = request.email)
        user.set_password(request.password)
        db.add(user)
        db.commit()
        db.refresh(user)
        
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Data")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Invalid Request: " + str(e))
    
    user_schema = UserResponseSchema.from_orm(user)
    # return Success
    return UserResponse(Status=Status.Success, User=user_schema)
    

@router.post('/auth/login', summary="Signin", response_model=UserLoginResponse)
def login(request : UserLoginSchema, db: Session = Depends(get_db)):
    try:
        user = db.query(Users).filter(Users.email == request.email).first()
        if user and user.check_password(request.password):
            # Get the access token using JWT to allow user to access the protected API
            access_token = create_access_token({"user":user.email})
        else:
            raise HTTPException(status_code=401, detail="Invalid Credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Invalid Request" )
    # return Success
    return UserLoginResponse(Status=Status.Success,access_token=access_token,token_type="bearer")


@router.get('/auth/me', summary="Check loggedIn user", response_model=UserResponse)
def loggedInUser( token=Depends(JWTBearer()),db: Session = Depends(get_db)):
    try:
        print("Token I am getting is ", token)
        token_data = verify_token(token)
        user = db.query(Users).filter(Users.email == token_data.user).first()
        if user:
            user_data = UserGlobalSchema.from_orm(user)
            # return {"Status":Status.Success,"User":user_data}
        else:
            raise HTTPException(status_code=404, detail="User not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail="Invalid Reuquest: "+ str(e))
    # return Success
    return UserResponse(Status=Status.Success, User=user_data)
        