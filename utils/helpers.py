from decimal import Decimal, ROUND_HALF_UP


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalize_payment_method(payment_method: str) -> str:
    return payment_method.strip().lower()


def is_valid_mobile(mobile: str) -> bool:
    return mobile.isdigit() and len(mobile) == 10


def is_valid_quantity(quantity: int) -> bool:
    return quantity > 0


def calculate_line_total(price, quantity: int) -> Decimal:
    line_total = Decimal(str(price)) * quantity

    return line_total.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


def calculate_order_total(cart_items) -> Decimal:
    total = Decimal("0.00")

    for cart_item in cart_items:
        total += calculate_line_total(
            cart_item.product.price,
            cart_item.quantity,
        )

    return total.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )