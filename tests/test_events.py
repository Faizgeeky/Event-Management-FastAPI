

#1.Add event (only Admin)
# test_events.py


def test_post_add_event(test_client, event_payload):
    # Perform login with the admin user credentials
    admin_login_payload = {
        "email": "admin@oolka.com",
        "password": "securepassword123"  # Use the correct password
    }

    response = test_client.post("/auth/login", json=admin_login_payload)
    assert response.status_code == 200
    response_json = response.json()
    assert "access_token" in response_json

    # Extract the access token from the response
    auth_token = response_json['access_token']
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }

    # Add an event using the admin token
    response = test_client.post("/event", json=event_payload, headers=headers)
    assert response.status_code == 201
    response_json = response.json()
    assert response_json["Status"] == "Success"  # Adjust based on actual response


# 2. Get all events
def test_get_all_events(test_client):
    response = test_client.get("/events")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json['Status'] == "Success"
    assert "Events" in response_json

# 3. Filter events
def test_get_event_by_id_200(test_client, event_id):
    response = test_client.get(f"/events/{event_id}")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json['Status'] == "Success"
    assert "Event" in response_json


def test_get_event_by_id_404(test_client):
    response = test_client.get("/event/10")
    assert response.status_code == 404   

# 4. Book events 
def test_book_event(test_client, event_id, admin_token):
    headers = {
        'Authorization': f'Bearer {admin_token}'
    }
    response = test_client.post(f"/events/{event_id}/book",
    headers=headers
     )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['Status'] == "Success"
    assert "payment_url" in response_json['Data'] 


def test_book_event_unauthorised(test_client, event_id, admin_token):
    headers = {
        'Authorization': f'Bearer wrong_token'
    }
    response = test_client.post(f"/events/{event_id}/book",
    headers=headers
     )
    assert response.status_code == 401
    
