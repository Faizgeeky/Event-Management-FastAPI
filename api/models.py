from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, CheckConstraint, Float
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
    latitude = Column(Float)
    longitude = Column(Float)
    available_tickets = Column(Integer)
    reserve_tickets = Column(Integer, default=0)
    price_per_ticket =  Column(Float)

    def check_add_tickets(self, available_tickets):
        if available_tickets <= 0:
            raise ValueError("Available tickets must be greater than 0.")
        self.available_tickets = available_tickets
    
    def check_add_ticket_price(self, price_per_ticket):
        if price_per_ticket <= 0:
            raise ValueError("Ticket price must be greater than 0.")
        self.price_per_ticket = price_per_ticket

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    number_of_tickets = Column(Integer)
    total_price = Column(Integer)
    event = relationship("Event")

# class Payments(Base)
