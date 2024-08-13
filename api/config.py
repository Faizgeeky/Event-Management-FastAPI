# app/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    DATABASE_URL = 'sqlite:///./event.db'
    # PAYMENT_GATEWAY_API_KEY = os.getenv("PAYMENT_GATEWAY_API_KEY")
    # GOOGLE_MAP_API_KEY = os.getenv("GOOGLE_MAP_API_KEY")
