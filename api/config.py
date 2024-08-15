import os
from dotenv import load_dotenv

load_dotenv()

# ADMIN_EMAIL = "admin@oolka.com"
# ADMIN_USERNAME="admin"
# ADMIN_PASSWORD="securepassword123"

# DATABASE_URL = "sqlite:///./events.db"
# JWT_SECRET_KEY = "lnbjlcbajld-ljncljkak-jkblknakn"
# ALGORITHM = "HS256"
# JWT_REFRESH_TOKEN_KEY = 'kjbjn0kjbklnasjnjnad'
# ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
# GOOGLE_MAPS_API_KEY = 'AIzaSyDlDDuDskYKKOhliC9Fa7c32xwie_KNVtI'
# PAYPAL_SECRET_KEY = 'EJfNOp3bXsWEivqLSc4U30x0XALiaYFfqnAM81ZpkGIpDgAqRB3OB5ENUQpVfpGyJhl3skFIWIaBHVZp'
# PAYPAL_CLIENT_ID = 'ARAYwlMxf7FqWaUmNAI7dDNF-fBJKPtFqWYf5yGgnDtsdMEUVWtFu71opWbcUvB7bN-9euuEUP641psv'
# PAYPAL_ENV = "sandbox" #sandbox or live Paypal envoirnment 
# PAYPAL_API_BASE_URL = "https://sandbox.paypal.com"
# HOST = "http://127.0.0.1:8000"

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