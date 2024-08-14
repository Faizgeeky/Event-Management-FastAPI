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