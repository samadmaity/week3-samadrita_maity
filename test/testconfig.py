from uuid import uuid4


def create_user_payload(
    password: str = "Password123",
) -> dict:
    return {
        "name": "Test User",
        "email": f"user_{uuid4().hex[:8]}@example.com",
        "password": password,
        "mobile": "9876543210",
    }
