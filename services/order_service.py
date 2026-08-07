from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from repositories.cart_repository import CartRepository
from repositories.order_repository import OrderRepository
from schemas.order_schema import OrderCreate
from utils.helpers import calculate_order_total


class OrderService:

    VALID_PAYMENT_METHODS = {
        "card",
        "cash",
        "upi",
    }

    def __init__(self):

        self.cart_repository = CartRepository()
        self.order_repository = OrderRepository()

    def _check_user_exists(
        self,
        db: Session,
        user_id: int,
    ):

        user = (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user

    def checkout(
        self,
        db: Session,
        order_data: OrderCreate,
    ):

        self._check_user_exists(
            db,
            order_data.user_id,
        )

        payment_method = order_data.payment_method.strip().lower()

        if payment_method not in self.VALID_PAYMENT_METHODS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment method must be card, cash, or upi",
            )

        cart_items = self.cart_repository.get_cart_items_with_products(
            db,
            order_data.user_id,
        )

        if not cart_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot checkout an empty cart",
            )

        total_amount = calculate_order_total(cart_items)
        validated_items = []

        for cart_item in cart_items:

            product = cart_item.product

            if product is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product not found for a cart item",
                )

            if cart_item.quantity <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cart quantity must be greater than zero",
                )

            if cart_item.quantity > product.available_quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        f"Insufficient stock for product "
                        f"'{product.product_name}'"
                    ),
                )

            product_price = Decimal(
                str(product.price),
            )

            item_total = product_price * cart_item.quantity
            total_amount += item_total

            validated_items.append(
                (
                    cart_item,
                    product,
                    product_price,
                )
            )

        try:

            new_order = self.order_repository.create_order(
                db=db,
                user_id=order_data.user_id,
                payment_method=payment_method,
                total_amount=total_amount,
            )

            order_id = new_order.order_id

            for cart_item, product, product_price in validated_items:

                self.order_repository.create_order_detail(
                    db=db,
                    order_id=order_id,
                    product_id=product.product_id,
                    quantity=cart_item.quantity,
                    price=product_price,
                )

                product.available_quantity -= cart_item.quantity

                db.delete(cart_item)

            self.order_repository.commit(db)

            return self.order_repository.get_order_by_id(
                db,
                order_id,
            )

        except HTTPException:
            self.order_repository.rollback(db)
            raise

        except Exception:
            self.order_repository.rollback(db)

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to place order",
            )

    def get_order_history(
        self,
        db: Session,
        user_id: int,
    ):

        self._check_user_exists(
            db,
            user_id,
        )

        return self.order_repository.get_orders_by_user(
            db,
            user_id,
        )

    def get_order_details(
        self,
        db: Session,
        order_id: int,
    ):

        order = self.order_repository.get_order_by_id(
            db,
            order_id,
        )

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

        return order
