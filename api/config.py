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

# DATABASE_URL = os.getenv("DATABASE_URL")
# STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
# GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
# SECRET_KEY = os.getenv("SECRET_KEY")
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
