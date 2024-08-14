'''
Written By : Faizmohammad Nandoliya
Last Updated     : 14-08-2024
Contact  : nandoliyafaiz429@gmail.com

'''

from fastapi import FastAPI
from .routes import index, auth, events
from .database import engine, Base
from .admin import create_admin_user
app = FastAPI()

Base.metadata.create_all(bind=engine)
create_admin_user()

# index test route
app.include_router(index.router)
# auth route
app.include_router(auth.router)
#events route
app.include_router(events.router)