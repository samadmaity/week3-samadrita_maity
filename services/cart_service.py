from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from repositories.cart_repository import CartRepository
from repositories.product_repository import ProductRepository
from schemas.cart_schema import (
    CartItemCreate,
    CartItemUpdate,
    CartSummaryResponse,
)


class CartService:

    def __init__(self):
        self.cart_repository = CartRepository()
        self.product_repository = ProductRepository()

    def _get_user_by_id(
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
                detail="You can access only your own cart",
            )

    def _get_owned_cart_item(
        self,
        db: Session,
        cart_item_id: int,
        current_user_id: int,
    ):
        cart_item = (
            self.cart_repository.get_cart_item_by_id(
                db,
                cart_item_id,
            )
        )

        if cart_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found",
            )

        if cart_item.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can access only your own cart item",
            )

        return cart_item

    def add_cart_item(
        self,
        db: Session,
        cart_item: CartItemCreate,
        current_user_id: int,
    ):
        # The user comes from the JWT token.
        self._get_user_by_id(db, current_user_id)

        product = (
            self.product_repository.get_product_by_id(
                db,
                cart_item.product_id,
            )
        )

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        if cart_item.quantity > product.available_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Requested quantity exceeds available stock",
            )

        existing_cart_item = (
            self.cart_repository
            .get_cart_item_by_user_and_product(
                db,
                current_user_id,
                cart_item.product_id,
            )
        )

        if existing_cart_item:
            new_quantity = (
                existing_cart_item.quantity
                + cart_item.quantity
            )

            if new_quantity > product.available_quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Total cart quantity exceeds available stock",
                )

            return self.cart_repository.update_cart_item(
                db,
                existing_cart_item,
                new_quantity,
            )

        return self.cart_repository.create_cart_item(
            db,
            current_user_id,
            cart_item,
        )

    def get_cart(
        self,
        db: Session,
        user_id: int,
        current_user_id: int,
    ):
        self._check_user_access(
            user_id,
            current_user_id,
        )

        self._get_user_by_id(db, current_user_id)

        return self.cart_repository.get_cart_items_by_user(
            db,
            current_user_id,
        )

    def update_cart_item(
        self,
        db: Session,
        cart_item_id: int,
        cart_item_data: CartItemUpdate,
        current_user_id: int,
    ):
        cart_item = self._get_owned_cart_item(
            db,
            cart_item_id,
            current_user_id,
        )

        product = (
            self.product_repository.get_product_by_id(
                db,
                cart_item.product_id,
            )
        )

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        if cart_item_data.quantity > product.available_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Requested quantity exceeds available stock",
            )

        return self.cart_repository.update_cart_item(
            db,
            cart_item,
            cart_item_data.quantity,
        )

    def remove_cart_item(
        self,
        db: Session,
        cart_item_id: int,
        current_user_id: int,
    ):
        cart_item = self._get_owned_cart_item(
            db,
            cart_item_id,
            current_user_id,
        )

        self.cart_repository.delete_cart_item(
            db,
            cart_item,
        )

        return {
            "message": "Cart item removed successfully",
        }

    def get_cart_summary(
        self,
        db: Session,
        user_id: int,
        current_user_id: int,
    ):
        self._check_user_access(
            user_id,
            current_user_id,
        )

        self._get_user_by_id(db, current_user_id)

        cart_items = (
            self.cart_repository
            .get_cart_items_with_products(
                db,
                current_user_id,
            )
        )

        total_items = len(cart_items)

        total_quantity = sum(
            item.quantity for item in cart_items
        )

        total_amount = Decimal("0.00")

        for item in cart_items:
            if item.product is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product associated with cart item was not found",
                )

            price = Decimal(str(item.product.price))
            total_amount += price * item.quantity

        return CartSummaryResponse(
            items=cart_items,
            total_items=total_items,
            total_quantity=total_quantity,
            total_amount=total_amount,
        )
