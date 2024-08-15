from fastapi import APIRouter
import os

router = APIRouter()

@router.get("/")
def index():
    return {"message":"API's are live on web!!!"+ str(os.getenv('DATABASE_URL'))}