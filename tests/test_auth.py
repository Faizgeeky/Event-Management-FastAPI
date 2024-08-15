
# Test successful registration (200 OK)
def test_register_user_success(test_client, user_payload):
    response = test_client.post("/auth/register", json=user_payload)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["Status"] == "Success"
    assert response_json["User"]["username"] == "Oolka_Test_User"
    assert response_json["User"]["email"] == "test@oolka.com"

# Without payload
def test_register_user_wrong_payload(test_client):
    response = test_client.post("/auth/register", json={})
    assert response.status_code == 422

# login with corret payload
def test_login_success(test_client,user_login_payload, user_payload):
    response = test_client.post("/auth/register", json=user_payload)
    assert response.status_code == 200
    response = test_client.post("/auth/login", json=user_login_payload)
    print("response ", response)
    assert response.status_code == 200
    response_json = response.json()
    assert "access_token" in response_json

# Invalid creds
def test_login_invalid_credentials(test_client,user_payload):
    response = test_client.post("/auth/register", json=user_payload)
    assert response.status_code == 200
    response = test_client.post("/auth/login", json={"email": "testuser@mail.com", "password": "wrongpassword"})
    assert response.status_code == 500
    response_json = response.json()
    assert response_json["detail"] == "Invalid Request"
