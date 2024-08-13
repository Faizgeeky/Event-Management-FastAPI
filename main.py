# main.py
from fastapi import FastAPI
from api.routes import router

app = FastAPI()

# Include routes from the routes module
# app.include_router(router)

# Optionally, include other configurations such as CORS, middleware, etc.
