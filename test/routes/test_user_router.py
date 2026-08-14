from test.testconfig import create_user_payload


REGISTER_URL = "/users/register"


def test_register_user_successfully(client):
    payload = create_user_payload()

    response = client.post(
        REGISTER_URL,
        json=payload,
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["user_id"] > 0
    assert response_data["name"] == "Test User"
    assert response_data["email"] == payload["email"]
    assert response_data["mobile"] == "9876543210"
    assert response_data["role"] == "customer"

    assert "password" not in response_data
    assert "password_hash" not in response_data


def test_duplicate_email_is_rejected(client):
    payload = create_user_payload()

    first_response = client.post(
        REGISTER_URL,
        json=payload,
    )

    assert first_response.status_code == 200

    second_response = client.post(
        REGISTER_URL,
        json=payload,
    )

    assert second_response.status_code == 400
    assert second_response.json()["detail"] == (
        "Email already exists"
    )


def test_invalid_email_is_rejected(client):
    payload = create_user_payload()
    payload["email"] = "invalid-email"

    response = client.post(
        REGISTER_URL,
        json=payload,
    )

    assert response.status_code == 422


def test_short_password_is_rejected(client):
    payload = create_user_payload(
        password="12345",
    )

    response = client.post(
        REGISTER_URL,
        json=payload,
    )

    assert response.status_code == 422

def test_mobile_with_wrong_length_is_rejected(client):
    payload = create_user_payload()
    payload["mobile"] = "12345"

    response = client.post(
        REGISTER_URL,
        json=payload,
    )

    assert response.status_code == 422


def test_empty_name_is_rejected(client):
    payload = create_user_payload()
    payload["name"] = ""

    response = client.post(
        REGISTER_URL,
        json=payload,
    )

    assert response.status_code == 422
