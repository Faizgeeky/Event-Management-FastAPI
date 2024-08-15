import pytest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from api.main import app
from api.database import Base, get_db
from api.admin import create_admin_user
from api.models import Users
# SQLite database URL for testing
SQLITE_DATABASE_URL = "sqlite:///./test.db"

# Create a SQLAlchemy engine
engine = create_engine(
    SQLITE_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create a sessionmaker to manage sessions
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables in the database
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Create a new database session with a rollback at the end of the test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function", autouse=True)
def setup_admin_user(db_session):
    """Create an admin user in the test database."""
    
    # Add an admin user
    admin_user = Users(
        username="admin",
        email="admin@oolka.com",
        is_admin = True  # Ensure this matches your hashing logic
    )
    admin_user.set_password(password="securepassword123")

    db_session.add(admin_user)
    db_session.commit()
        


@pytest.fixture(scope="function")
def test_client(db_session):
    """Create a test client that uses the override_get_db fixture to return a session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client

# Fixture to generate a user payload
@pytest.fixture()
def user_payload():
    return {
        "username": "Oolka_Test_User",
        "email": "test@oolka.com",
        "password": "Password",
    }

@pytest.fixture()
def user_login_payload():
    return {
        "email": "test@oolka.com",
        "password": "Password",
    }

@pytest.fixture()
def admin_payload():
    return{
        "email": "admin@oolka.com",
        "password":"securepassword123"
    }

@pytest.fixture()
def event_payload():
    return {
    "name":"Credit Card  - Oolka Season-2",
    "date" :"2025-09-20T17:30:00",
    "location":"Oolka - Credit Score Builder",
    "available_tickets": 85,
    "price_per_ticket" : 49
}