from decimal import Decimal
from uuid import uuid4

from app.models.cart import CartItem
from app.models.category import Category
from app.models.product import Product


REGISTER_URL = "/users/register"
LOGIN_URL = "/auth/login"
CART_ADD_URL = "/cart/add"
CHECKOUT_URL = "/orders/checkout"


def create_user_payload() -> dict:
    return {
        "name": "Order Test User",
        "email": f"order_{uuid4().hex[:8]}@example.com",
        "password": "Password123",
        "mobile": "9876543210",
    }


def register_and_login(client):
    payload = create_user_payload()

    register_response = client.post(
        REGISTER_URL,
        json=payload,
    )

    assert register_response.status_code in (200, 201)

    user_data = register_response.json()

    login_response = client.post(
        LOGIN_URL,
        data={
            "username": payload["email"],
            "password": payload["password"],
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}",
    }

    return user_data, headers


def seed_category(db_session) -> Category:
    category = Category(
        category_name=f"Category {uuid4().hex[:8]}",
    )

    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    return category


def seed_product(
    db_session,
    category: Category,
    quantity: int = 10,
) -> Product:
    product = Product(
        product_name=f"Product {uuid4().hex[:8]}",
        description="Order test product",
        category=category,
        price=Decimal("25.50"),
        available_quantity=quantity,
        product_url="https://example.com/product",
    )

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    return product


def add_product_to_cart(
    client,
    product: Product,
    headers: dict,
    quantity: int = 2,
):
    response = client.post(
        CART_ADD_URL,
        json={
            "product_id": product.product_id,
            "quantity": quantity,
        },
        headers=headers,
    )

    assert response.status_code in (200, 201)

    return response.json()


def create_order_flow(
    client,
    db_session,
):
    user_data, headers = register_and_login(client)

    category = seed_category(db_session)

    product = seed_product(
        db_session,
        category,
    )

    add_product_to_cart(
        client,
        product,
        headers,
        quantity=2,
    )

    checkout_response = client.post(
        CHECKOUT_URL,
        json={
            "payment_method": "card",
        },
        headers=headers,
    )

    assert checkout_response.status_code in (200, 201)

    return (
        user_data,
        headers,
        product,
        checkout_response.json(),
    )


def test_checkout_requires_authentication(client):
    response = client.post(
        CHECKOUT_URL,
        json={
            "payment_method": "card",
        },
    )

    assert response.status_code == 401


def test_checkout_empty_cart_is_rejected(client):
    _, headers = register_and_login(client)

    response = client.post(
        CHECKOUT_URL,
        json={
            "payment_method": "card",
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Cannot checkout an empty cart"
    )


def test_invalid_payment_method_is_rejected(client):
    _, headers = register_and_login(client)

    response = client.post(
        CHECKOUT_URL,
        json={
            "payment_method": "bitcoin",
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Payment method must be card, cash, or upi"
    )


def test_successful_checkout(
    client,
    db_session,
):
    user_data, _, product, order = create_order_flow(
        client,
        db_session,
    )

    assert order["order_id"] > 0
    assert order["user_id"] == user_data["user_id"]
    assert order["payment_method"] == "card"

    assert Decimal(
        str(order["total_amount"]),
    ) == Decimal("51.00")

    assert len(order["order_details"]) == 1

    order_detail = order["order_details"][0]

    assert order_detail["product_id"] == product.product_id
    assert order_detail["quantity"] == 2
    assert Decimal(
        str(order_detail["price"]),
    ) == Decimal("25.50")


def test_checkout_reduces_stock_and_clears_cart(
    client,
    db_session,
):
    user_data, _, product, _ = create_order_flow(
        client,
        db_session,
    )

    db_session.expire_all()

    updated_product = (
        db_session.query(Product)
        .filter(
            Product.product_id == product.product_id,
        )
        .first()
    )

    assert updated_product is not None
    assert updated_product.available_quantity == 8

    remaining_cart_items = (
        db_session.query(CartItem)
        .filter(
            CartItem.user_id == user_data["user_id"],
        )
        .all()
    )

    assert remaining_cart_items == []


def test_get_order_history(
    client,
    db_session,
):
    user_data, headers, _, order = create_order_flow(
        client,
        db_session,
    )

    response = client.get(
        f"/orders/{user_data['user_id']}",
        headers=headers,
    )

    assert response.status_code == 200

    orders = response.json()

    assert len(orders) == 1
    assert orders[0]["order_id"] == order["order_id"]


def test_get_order_details(
    client,
    db_session,
):
    _, headers, _, order = create_order_flow(
        client,
        db_session,
    )

    response = client.get(
        f"/orders/details/{order['order_id']}",
        headers=headers,
    )

    assert response.status_code == 200

    order_data = response.json()

    assert order_data["order_id"] == order["order_id"]
    assert len(order_data["order_details"]) == 1


def test_get_order_history_requires_authentication(client):
    response = client.get("/orders/1")

    assert response.status_code == 401


def test_get_order_details_requires_authentication(client):
    response = client.get("/orders/details/1")

    assert response.status_code == 401


def test_order_details_not_found(client):
    _, headers = register_and_login(client)

    response = client.get(
        "/orders/details/999999",
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"


def test_user_cannot_access_another_users_order(
    client,
    db_session,
):
    first_user, _, _, order = create_order_flow(
        client,
        db_session,
    )

    _, second_user_headers = register_and_login(client)

    history_response = client.get(
        f"/orders/{first_user['user_id']}",
        headers=second_user_headers,
    )

    assert history_response.status_code == 403

    details_response = client.get(
        f"/orders/details/{order['order_id']}",
        headers=second_user_headers,
    )

    assert details_response.status_code == 403
