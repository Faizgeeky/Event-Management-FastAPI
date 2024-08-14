from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base
from werkzeug.security import generate_password_hash, check_password_hash

class Users(Base):
    __tablename__= "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, min_length=4 , max_length=100)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(128), nullable=False, min_length = 5)
    is_admin = Column(Boolean, default=False)
  

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(DateTime)
    location = Column(String)
    available_tickets = Column(Integer)

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    number_of_tickets = Column(Integer)
    total_price = Column(Integer)
    event = relationship("Event")
