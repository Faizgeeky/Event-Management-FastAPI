from fastapi import APIRouter


router = APIRouter()

@router.get("/")
def index():
    return {"message":"API's are live on web!!!"}