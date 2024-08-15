from fastapi import APIRouter
import os

router = APIRouter()

@router.get("/",
          summary="Index Endpoint", 
          description="Hit '/' to test if api's Live", 
          response_description="index route")
def index():
    return {"message":"API's are live on web!!!"+ str(os.getenv('DATABASE_URL'))}