from fastapi import APIRouter, Depends, HTTPException, Request, Query
from .auth import verify_token, oauth2_scheme
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from api.database import get_db
from api.models import Users, Event, Booking
import requests
from api.schema import EventSchema, EventGlobalSchema, BookingSchema
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
    print("data is", data)
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        # reaise error here TEMP returning Oolka cordinates
        return 12.925738470141543, 77.67473271259571

# @router.post('/event')
# def add_event(request : EvntSchema, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db) ):
    

@router.post('/event')
def add_event(event : EventSchema,token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    latitude, longitude = geocode_address(event.location)
    
    decoded_token = verify_token(token)

    user = db.query(Users).filter(Users.email == decoded_token.user).first()
    try:
        if user.is_admin and latitude != None and longitude != None:
            db_event = Event(name = event.name, date = event.date, location = event.location, latitude = latitude, longitude =  longitude)
            db_event.check_add_ticket_price(price_per_ticket = event.price_per_ticket)
            db_event.check_add_tickets(available_tickets = event.available_tickets)
            db.add(db_event)
            db.commit()
            db.refresh(db_event)
            return {"message": "Event added successfully", "data":db_event}

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

       

@router.get('/events')
def fetch_events( db: Session = Depends(get_db)):
    # fetch all events 
    try:
        events = db.query(Event).all()
        return {"message": "Events fetched successfully", "data": events}

    except SQLAlchemyError as se:
       raise HTTPException(status_code=500, detail="Database error: " + str(se))

    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))


    
@router.get('/events/{event_id}')
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
    if event_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid event ID. ID must be a positive integer.")
    query_params = request.query_params
    print("data is here ", query_params)

    # set defaut booking ticket is 1 
    ticket_quantity = 1
    
    try:
        # ticket quantity available in param update quantity
        if 'ticket_quantity' in query_params:
            if int(query_params['ticket_quantity']) >0:
                ticket_quantity = int(query_params['ticket_quantity'])
            else:
                raise HTTPException(status_code=400, detail=f"Invalid Ticket Quantity")
        print("check point 1")
        # get event by id
        event = db.query(Event).filter(Event.id == event_id).first()
        if event is None:
            raise HTTPException(status_code=404, detail=f"Event with ID {event_id} not found.")
        print("check point 2")
        
        # check if avaliable tickets are more than ticket quantity
        if int(event.available_tickets) < ticket_quantity:
            raise HTTPException(status_code=400, detail=f"Only {event.available_tickets} left")
        print("check point 3", type(event.date))
        
        # check if event date is not past
        if event.date < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Event is closed for booking.")
        print("check point 4")
        
        event.reserve_tickets =  event.reserve_tickets + ticket_quantity
        event.available_tickets = event.available_tickets - ticket_quantity
        
        # Generate PayPal payment URL
        
        payment = Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": f"{HOST}/success/?jwt_token={token}",
                "cancel_url": f"{HOST}/cancel?jwt_token={'kjbk'}"
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
        print("payment", payment)
        if payment.create():
            #  commit the changes from 
            db.commit()
            db.refresh(event) 

            db_booking = Booking(event_id=event.id,user_id=1, number_of_tickets=ticket_quantity, total_price= (event.price_per_ticket * ticket_quantity), order_status="processing" )
            db.add(db_booking)
            db.commit()
            db.refresh(db_booking)


            

            for link in payment.links:
                if link.rel == "approval_url":
                    print("data ", link)
                    return {"data":link.href, "message":"payment link generated successfully"}
        else:
            db.rollback()
            raise HTTPException(status_code=500, detail="PayPal payment creation failed.")
            
    except SQLAlchemyError as se:
       raise HTTPException(status_code=500, detail="Database error: " + str(se))

    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))



@router.get('/success')
async def success_payment(paymentId: str, PayerID: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    # Handle payment confirmation here
    try:
        payment = Payment.find(paymentId)
        print("Payment id ", payment)
        if payment.execute({"payer_id": PayerID}):
            # reservation = db.query(TicketReservation).filter(
            #     TicketReservation.status == 'reserved',
            #     TicketReservation.id == payment.transactions[0].item_list.items[0].sku
            # ).first()

            # if not reservation:
            #     raise HTTPException(status_code=404, detail="Reservation not found.")
            
            # Confirm the reservation
            # reservation.status = 'paid'
            # event = db.query(Event).filter(Event.id == reservation.event_id).first()
            if 1==1:
                # event.available_tickets -= reservation.reserved_tickets
                db.commit()
                return {"message": "Booking confirmed successfully"}
            else:
                raise HTTPException(status_code=404, detail="Event not found.")
        else:
            raise HTTPException(status_code=400, detail="Payment not completed.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))

@router.get('/cancel')
async def cancel(request: Request):
    # print("token is ",jwt)
    return {"message": "Payment was canceled. Please try again if you wish to complete the transaction."}
    
""" 
1. Accept book request 
2. Check tickets avaibale 
3. Check event exisit 
4. Create and reserve tickets until the payment has been made 1 minutes 
5. If payment is succesfull - remove reserved tickets 
6. If payment is failed - remove reserved tickets and add it in total tickets 
"""