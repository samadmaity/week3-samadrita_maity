from decimal import Decimal

from utils.logger import logger


def send_order_confirmation(
    order_id: int,
    user_id: int,
    total_amount: Decimal,
) -> None:
    """Simulate sending an order confirmation notification."""

    logger.info(
        "Order confirmation sent: order_id=%s user_id=%s total_amount=%s",
        order_id,
        user_id,
        total_amount,
    )
