# Event Management API using FastAPI and PayPal Payment Gateway

###  Features

- **Authentication**: Users can log in using JWT (JSON Web Tokens) for secure authentication.
- **Adding Events**: Admin can only add the events if loggedIn
- **Fethcing Events**: Users can easily access all the events
- **Filter Events**: Users can easily filer the events
- **Booking Events**: Users can book any future event with custom Ticket quantity
- **PayPal**: Users can make payment to confirm the Bookings


### Blog on How this API's are designed 

    https://indigo-lord-166.notion.site/Event-Booking-Oolka-backend-task-44c10de260994bc8bfec09d488c31e1e?pvs=25


### Demonstration Video for this API's

    https://www.canva.com/design/DAGN_b4twU4/6YGLAi6kNWIewYf51IoJrA/watch?utm_content=DAGN_b4twU4&utm_campaign=designshare&utm_medium=link&utm_source=editor


## Setup Instructions

### Clone the Repository

To get started, clone the repository to your local machine:

```sh
git clone https://github.com/Faizgeeky/Event-Management-FastAPI.git
cd Event-Management-FastAPI
```

### Setting Up the Server



1. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

2. Setup .env file or export all variables:
    ```sh
    
    # Admin credentials
    ADMIN_EMAIL=admin_email
    ADMIN_USERNAME=admin_username
    ADMIN_PASSWORD=securepassword

    # Database URL
    DATABASE_URL=database_uri

    # JWT settings
    JWT_SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30

    # Google Maps API key
    GOOGLE_MAPS_API_KEY=your_google_map_api

    # PayPal settings
    PAYPAL_SECRET_KEY=your_secret_key_paypal
    PAYPAL_CLIENT_ID=your_client_id
    PAYPAL_ENV=sandbox
    PAYPAL_API_BASE_URL=https://sandbox.paypal.com

    # Application host
    HOST=http://127.0.0.1:8000
    ```


###   🚀🚀 Ready to launch your API Endpoints

4. Run uvicorn server:
    ```sh
    uvicorn api.main:app --reload 
    ```

### API's

 ```sh
    /auth/register
    /auth/login

    POST /event/ 
    GET /events/ 
    GET /events/{event_id}
    POST /events/{event_id}/book
    GET /success
    GET /cancel
 ``` 

###   🚀🚀 Test all API's using pytest

5. Run API testing :
    ```sh
    pytest 
    ```
   

### Postman Collection

A `Ookla-Event-API.postman_collection.json` file is included for easy testing of the API endpoints with Postman. Simply import this file into Postman to get started.

 
### API Postman collection

* It has all the api's endpoint with request and response
* You can import it in postman and use it to test the api's


### Enhancement 

- Security
    - Encryption of data passing to PayPal payment url
        - currently it looks like [***https://sandbox.paypal.com/payment_id=111,event_id=1,token=jklncjbda,booking_id=2](https://sandbox.paypal.com/payment_id=111,event_id=1,token=jklncjbda,booking_id=2)***  data can be easily readable to any user including jwt token
        - after encryption with secure key it will look like [https://sandbox.paypal.com/payment_id=111,event_id=1,token=VEADdaljbnjkac,booking_id=](https://sandbox.paypal.com/payment_id=111,event_id=1,token=jklncjbda,booking_id=2)bjac basically not readable and hard to break
        
- Database refresh using time or Message broker
    - Currently what if payment link is generated but user has not clicked (canceled / succeed) payment
    - our database doesn’t know about that which can lead us to inaccurate data
    
- Limitation
    - Limiting the quantity of bookings per user , per event , etc


# Docker Setup 

## Building and Running the Docker Container

### Docker Build and Run

1. **Build the Docker Image**

   Build the Docker image using the following command:

   ```sh
   docker build -t oolka_app .
   ```

2. **Run the Docker Container**

  Run the Docker container with the environment variables from the .env file and map port 8000 to your local machine:

    
    Copy code
    docker run --env-file .env -p 8000:8000 oolka_app
    Access the application at http://127.0.0.1:8000/.
    

### Docker compose 

    
    docker-compose build
    docker-compose up
    


### API Documentations 

- It can be downloaded and test live while running the api's on webbrowser 

    <!-- API Testing -->
    http://127.0.0.0:8000/docs 

    <!-- API Documentation -->
    http://127.0.0.0:8000/redoc
