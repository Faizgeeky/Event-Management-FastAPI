def test_whoami(test_client,user_login_payload, user_payload):
    response = test_client.post("/auth/register", json=user_payload)
    assert response.status_code == 200
    response = test_client.post("/auth/login", json=user_login_payload)
    print("response ", response)
    assert response.status_code == 200
    response_json = response.json()
    assert "access_token" in response_json
    auth_token = response_json['access_token']
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    response = test_client.get("/auth/me", headers=headers)
    print("response ", response)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["Status"] == "Success"
    assert response_json["User"]["username"] == "Oolka_Test_User"
    assert response_json["User"]["email"] == "test@oolka.com"


