import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_EMAIL = "admin@oolka.com"
ADMIN_USERNAME="admin"
ADMIN_PASSWORD="securepassword123"

DATABASE_URL = "sqlite:///./events.db"
JWT_SECRET_KEY = "lnbjlcbajld-ljncljkak-jkblknakn"
ALGORITHM = "HS256"
JWT_REFRESH_TOKEN_KEY = 'kjbjn0kjbklnasjnjnad'
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
GOOGLE_MAPS_API_KEY = 'AIzaSyDlDDuDskYKKOhliC9Fa7c32xwie_KNVtI'
PAYPAL_SECRET_KEY = 'EJfNOp3bXsWEivqLSc4U30x0XALiaYFfqnAM81ZpkGIpDgAqRB3OB5ENUQpVfpGyJhl3skFIWIaBHVZp'
PAYPAL_CLIENT_ID = 'ARAYwlMxf7FqWaUmNAI7dDNF-fBJKPtFqWYf5yGgnDtsdMEUVWtFu71opWbcUvB7bN-9euuEUP641psv'
PAYPAL_ENV = "sandbox" #sandbox or live Paypal envoirnment 
PAYPAL_API_BASE_URL = "https://sandbox.paypal.com"
HOST = "http://127.0.0.1:8000"