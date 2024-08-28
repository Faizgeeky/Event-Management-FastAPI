import os
from dotenv import load_dotenv

load_dotenv()



ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL")
ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD")

# Database URL
DATABASE_URL: str = os.getenv("DATABASE_URL")

# JWT settings
JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
ALGORITHM: str = os.getenv("ALGORITHM")
JWT_REFRESH_TOKEN_KEY: str = os.getenv("JWT_REFRESH_TOKEN_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Google Maps API key
GOOGLE_MAPS_API_KEY: str = os.getenv("GOOGLE_MAPS_API_KEY")

# PayPal settings
PAYPAL_SECRET_KEY: str = os.getenv("PAYPAL_SECRET_KEY")
PAYPAL_CLIENT_ID: str = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_ENV: str = os.getenv("PAYPAL_ENV")
PAYPAL_API_BASE_URL: str = os.getenv("PAYPAL_API_BASE_URL")

# Application host
HOST: str = os.getenv("HOST")