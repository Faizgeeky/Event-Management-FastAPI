

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
# 3. Filter events

# 4. Book events 

# 5. Cancel payment

# 6. Success payment 