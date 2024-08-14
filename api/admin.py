from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
from .database import engine
from .models import Users
from .config import ADMIN_EMAIL , ADMIN_PASSWORD , ADMIN_USERNAME

# Create the FastAPI app
app = FastAPI()

# Setup database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_admin_user():
    db = SessionLocal()

    # Check if the admin user already exists
    existing_admin = db.query(Users).filter_by(email=ADMIN_EMAIL).first()

    if not existing_admin:
        # Create a new admin user
        new_admin = Users(
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            is_admin=True
        )
        new_admin.set_password(ADMIN_PASSWORD)
        db.add(new_admin)
        db.commit()
        print(f"Admin user created:\nUsername: {ADMIN_USERNAME}\nEmail: {ADMIN_EMAIL}\nPassword: {ADMIN_PASSWORD}")
    else:
        print(f"Admin user with email {ADMIN_EMAIL} already exists: {existing_admin.username}")

    db.close()