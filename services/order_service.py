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

    def _check_user_access(
        self,
        requested_user_id: int,
        current_user_id: int,
    ):
        if requested_user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can access only your own orders",
            )

    def checkout(
        self,
        db: Session,
        order_data: OrderCreate,
        current_user_id: int,
    ):
        self._check_user_exists(
            db,
            current_user_id,
        )

        payment_method = (
            order_data.payment_method.strip().lower()
        )

        if payment_method not in self.VALID_PAYMENT_METHODS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment method must be card, cash, or upi",
            )

        cart_items = (
            self.cart_repository
            .get_cart_items_with_products(
                db,
                current_user_id,
            )
        )

        if not cart_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot checkout an empty cart",
            )

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

            validated_items.append(
                (
                    cart_item,
                    product,
                    product_price,
                )
            )

        # Calculate the total only once.
        total_amount = calculate_order_total(cart_items)

        try:
            new_order = self.order_repository.create_order(
                db=db,
                user_id=current_user_id,
                payment_method=payment_method,
                total_amount=total_amount,
            )

            for cart_item, product, product_price in validated_items:
                self.order_repository.create_order_detail(
                    db=db,
                    order_id=new_order.order_id,
                    product_id=product.product_id,
                    quantity=cart_item.quantity,
                    price=product_price,
                )

                product.available_quantity -= cart_item.quantity
                db.delete(cart_item)

            self.order_repository.commit(db)

            return self.order_repository.get_order_by_id(
                db,
                new_order.order_id,
            )

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
        current_user_id: int,
    ):
        self._check_user_access(
            user_id,
            current_user_id,
        )

        self._check_user_exists(
            db,
            current_user_id,
        )

        return self.order_repository.get_orders_by_user(
            db,
            current_user_id,
        )

    def get_order_details(
        self,
        db: Session,
        order_id: int,
        current_user_id: int,
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

        if order.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can access only your own order",
            )

        return order
