'''
Written By : Faizmohammad Nandoliya
Last Updated     : 14-08-2024
Contact  : nandoliyafaiz429@gmail.com

NOTE : In function 'geocode_address' I have handled "else" block manually kindly change that in production. 
(I did beacuse I had no working Google map API)
'''

from fastapi import APIRouter, Depends, HTTPException, Request, Query, Response
from .auth import verify_token, oauth2_scheme
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from api.database import get_db
from api.models import Users, Event, Booking
import requests
from api.schema import EventSchema, EventGlobalSchema, BookingSchema, PaymentStatus
from datetime import datetime
from api.config import GOOGLE_MAPS_API_KEY, PAYPAL_SECRET_KEY, PAYPAL_CLIENT_ID, PAYPAL_ENV, HOST
import paypalrestsdk
from paypalrestsdk import Payment


paypalrestsdk.configure({
  "mode": PAYPAL_ENV, # sandbox or live
  "client_id": PAYPAL_CLIENT_ID,
  "client_secret": PAYPAL_SECRET_KEY })

router = APIRouter()

def geocode_address(address: str):
    url = f"https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': address,
        'key': GOOGLE_MAPS_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        # raise error here TEMPORARY returning Oolka office cordinates
        return 12.925738470141543, 77.67473271259571

# get the current loggedIn user from token decoding and model
def get_current_user(token):
    decoded_token = verify_token(token)
    db = next(get_db())
    user = db.query(Users).filter(Users.email == decoded_token.user).first()
    return user


@router.post('/event',status_code=201)
def add_event(event : EventSchema,token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    latitude, longitude = geocode_address(event.location)
    
    user = get_current_user(token)
    try:
        if user.is_admin and latitude != None and longitude != None:
            db_event = Event(name = event.name, date = event.date, location = event.location, latitude = latitude, longitude =  longitude)
            db_event.check_add_ticket_price(price_per_ticket = event.price_per_ticket)
            db_event.check_add_tickets(available_tickets = event.available_tickets)
            db.add(db_event)
            db.commit()
            db.refresh(db_event)
            return {"message": "Event created successfully", "data":db_event}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Invalid data: {ve}")

    except IntegrityError as ie:
        db.rollback()  
        raise HTTPException(status_code=409, detail="Database integrity error: " + str(ie))

    except SQLAlchemyError as se:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(se))

    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))

       

@router.get('/events',status_code=200)
def fetch_events( db: Session = Depends(get_db)):
    # fetch all events 
    try:
        events = db.query(Event).all()
        return {"message": "Events fetched successfully", "data": events}

    except SQLAlchemyError as se:
       raise HTTPException(status_code=500, detail="Database error: " + str(se))

    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))


    
@router.get('/events/{event_id}',status_code=200)
def fetch_events(event_id: int, db: Session = Depends(get_db)):
    if event_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid event ID. ID must be a positive integer.")
    # fetch event by event id
    try:
        event = db.query(Event).filter(Event.id == event_id).first()
        if event is None:
            raise HTTPException(status_code=404, detail=f"Event with ID {event_id} not found.")
        return {"message": "Event fetched successfully", "data": event}
        
    except SQLAlchemyError as se:
       raise HTTPException(status_code=500, detail="Database error: " + str(se))

    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))


@router.post('/events/{event_id}/book')
async def book_event(event_id: int,
    request: Request,
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)):

    """ 
    Flow to book event 
    1. Check if Ticket quantity is there else set default 1
    2. Check if Even exisit 
    3. Check if even date is not passed 
    4.  Check if user has pending or processing payments with other or same events
    5. Check if ticket available based on quantity
    6. Deduct required tickets from total ticket and  add it in reserve tickets 
    7. Add booking and set status to Processing 
    8. Genetate payment url (add success , cancel payment url's)

    """

    if event_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid event ID. ID must be a positive integer.")
    query_params = request.query_params
    
    # get current user 
    user = get_current_user(token)
   
    # set defaut booking ticket is 1 
    ticket_quantity = 1
    
    try:
        # 1. Check if Ticket quantity is there else set default 1
        if 'ticket_quantity' in query_params:
            if int(query_params['ticket_quantity']) >0:
                ticket_quantity = int(query_params['ticket_quantity'])
            else:
                raise HTTPException(status_code=400, detail=f"Invalid Ticket Quantity")
        
        # 2.Check if Even exisit 
        event = db.query(Event).filter(Event.id == event_id).first()
        if event is None:
            raise HTTPException(status_code=404, detail=f"Event with ID {event_id} not found.")
        
        # 3.Check if even date is not passed 
        if event.date < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Event is closed for booking.")
        
        # 4.  Check if user has pending or processing payments with other or same events
        previous_booking = db.query(Booking).filter(Booking.user_id == user.id , Booking.order_status == PaymentStatus.PENDING).first()
        if previous_booking:
            raise HTTPException(status_code=400, detail=f"Cannot process more than 1 order")

        # 5.check if avaliable tickets are more than ticket quantity
        if int(event.available_tickets) < ticket_quantity:
            raise HTTPException(status_code=400, detail=f"Only {event.available_tickets} left")
                
        # 6.Deduct required tickets from total ticket and  add it in reserve tickets 
        event.reserve_tickets =  event.reserve_tickets + ticket_quantity
        event.available_tickets = event.available_tickets - ticket_quantity
        db.commit()
        db.refresh(event) 
        
        # 7. Add booking and set status to Processing 
        db_booking = Booking(event_id=event.id,user_id=user.id, number_of_tickets=ticket_quantity, total_price= (event.price_per_ticket * ticket_quantity), order_status=PaymentStatus.PENDING )
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)

        # 8. Genetate payment url (add success , cancel payment url's)
        payment = Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                # Add jwt token , booking_id , event_id - using which current order can be handled
                "return_url": f"{HOST}/success/?event_id={event.id}&booking_id={db_booking.id}&jwt_token={token}",
                "cancel_url": f"{HOST}/cancel/?event_id={event.id}&booking_id={db_booking.id}&jwt_token={token}"
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": f"Tickets for Event {event_id}",
                        "sku": "item",
                        "price": event.price_per_ticket,  # Example amount, adjust as needed
                        "currency": "USD",
                        "quantity": ticket_quantity
                    }]
                },
                "amount": {
                    "total": f"{event.price_per_ticket * ticket_quantity}",
                    "currency": "USD"
                },
                "description": "Booking tickets."
            }]
        })

        try:
            # filter out the Payment object
            if payment.create():
                for link in payment.links:
                    if link.rel == "approval_url":
                        return {"payment_url": link.href}
            else:
                error_message = payment.error['message'] if 'message' in payment.error else str(payment.error)
                raise HTTPException(status_code=500, detail=f"PayPal payment creation failed: {error_message}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

    except SQLAlchemyError as se:
       raise HTTPException(status_code=500, detail="Database error: " + str(se))

    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))



@router.get('/success', status_code=200)
async def success_payment(paymentId: str,
                        PayerID: str,
                        booking_id : str,
                        event_id : str,
                        jwt_token: str, 
                        db: Session = Depends(get_db)):
    """ 
    Flow:
    1.Verify token
    2.Verify payment id
    3.Check Booking by id
    4.Check event by id
    5.Update Payment status to "successful"
    6.Update - deduct booked tickets from Event reserve tickets
    7.Commit and return 200 message
    """
    # 1.Verify token
    user = get_current_user(jwt_token)
    try:
        if user:
            # 2.Verify payment id
            payment = Payment.find(paymentId)
            if payment is None:
                raise HTTPException(status_code=404, detail="Payment not found")

            if payment.execute({"payer_id":PayerID}):
                # 3.Check Booking by id
                booking_db = db.query(Booking).filter(Booking.id == booking_id, Booking.order_status == PaymentStatus.PENDING, Booking.user_id == user.id, Booking.event_id == event_id).first()
                if booking_db is None:
                    raise HTTPException(status_code=400, detail="Invalid booking request. No booking found for the provided payment ID.")
                
                # 4.Check event by id
                event_db = db.query(Event).filter(Event.id == booking_db.event_id).first()
                if event_db is None:
                    raise HTTPException(status_code=404, detail="Event not found")
                # 5.Update - deduct booked tickets from Event reserve tickets
                event_db.reserve_tickets -= booking_db.number_of_tickets
                # 6.Update Payment status to "successful"
                booking_db.order_status = PaymentStatus.SUCCESS
                
                # 7.Commit and return 200 message
                db.commit()
                db.refresh(booking_db)
                db.refresh(event_db)
                
                return {"message": f"Payment successful", 
                            "data":{"ticket_quantity":booking_db.number_of_tickets,
                            "event_name":event_db.name,
                            "booking_id":booking_db.id}}

            else:
                raise HTTPException(status_code=404, detail="Payment failed")
        else:
            raise HTTPException(status_code=401, detail="Unauthorized access")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))


@router.get('/cancel',status_code=200)
async def cancel(request: Request,booking_id : str, jwt_token: str, db: Session = Depends(get_db)):
    """ 
    Flow:
    1. Check if token is valid and filter user
    2. If user exisit continue
    3. Check if booking data exisit based on booking id in url req with user and payment status matched
    4. Check if event exist with same id
    5. Update total tickets summinng canceled tickets 
    6. Update reserve tickets by subtracting canceled tickets 
    7. Commit and responde
    """
    user = get_current_user(jwt_token)
    if user:
        try:
            booking_db = db.query(Booking).filter(Booking.id == booking_id, Booking.user_id == user.id, Booking.order_status == PaymentStatus.PENDING ).first()
            if booking_db is None:
                raise HTTPException(status_code=400, detail="Booking data not found" )
            
            event_db = db.query(Event).filter(Event.id == booking_db.event_id).first()
            if event_db is None:
                raise HTTPException(status_code=400, detail="Event data not found" )
            
            event_db.available_tickets += booking_db.number_of_tickets
            event_db.reserve_tickets -= booking_db.number_of_tickets
            
            booking_db.order_status = PaymentStatus.FAILED
            db.commit()
            db.refresh(event_db)
            db.refresh(booking_db)
            return {"message":f"Booking canceld for the Event {event_db.name}"}

        except Exception as e:
            raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))
    else:
        raise HTTPException(status_code=401, detail="Unauthorized access")
            
    
    


""" 
1. Accept book request  - Done
2. Check tickets avaibale  - Done
3. Check event exisit  - Done 
4. Create and reserve tickets until the payment has been made 1 minutes // Enhancement
5. If payment is succesfull - remove reserved tickets  
6. If payment is failed - remove reserved tickets and add it in total tickets 
"""


"""" 
Enhancement :
1. When payment url is unclicked 
2. When user land on cancel or success with expire token 
3. If same user has pending orders with same event or new event - take care of this so total tickets stays accurate
4. Limit the booking tickets so not single person can buy each ticket at a time
"""