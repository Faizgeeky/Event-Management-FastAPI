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
PAYPAL_SECRET_KEY = 'EKuAIit2m3925z2tjM61OUyb_gcmcHVxRxm5pyvPP-ar1xTv0oOJVDPIH80gAaMN9TyZ2GL5qjtcsdqE'
PAYPAL_CLIENT_ID = 'ASTQrQsV3-k52SFUPiJFzFV4hLrfj00P2FJ4rK8naK06FYeH45ez2JJDXkIS_AB6z8okwXBx2Is7_jJa'
PAYPAL_ENV = "sandbox" #sandbox or live Paypal envoirnment 
HOST = "http://127.0.0.1:8000"