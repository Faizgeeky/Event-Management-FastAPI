from fastapi import APIRouter, Depends
from .auth import verify_token, oauth2_scheme
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from database import get_db
router = APIRouter()


@router.post('/event')
def add_event(request : EvntSchema, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db) )