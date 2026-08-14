from sqlalchemy.orm import Session, joinedload

from app.models.cart import CartItem
from schemas.cart_schema import CartItemCreate


class CartRepository:

    def create_cart_item(
        self,
        db: Session,
        user_id: int,
        cart_item: CartItemCreate,
    ):
        new_cart_item = CartItem(
            user_id=user_id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
        )

        db.add(new_cart_item)
        db.commit()
        db.refresh(new_cart_item)

        return new_cart_item

    def get_cart_item_by_id(
        self,
        db: Session,
        cart_item_id: int,
    ):
        return (
            db.query(CartItem)
            .filter(CartItem.cart_item_id == cart_item_id)
            .first()
        )

    def get_cart_item_by_user_and_product(
        self,
        db: Session,
        user_id: int,
        product_id: int,
    ):
        return (
            db.query(CartItem)
            .filter(
                CartItem.user_id == user_id,
                CartItem.product_id == product_id,
            )
            .first()
        )

    def get_cart_items_by_user(
        self,
        db: Session,
        user_id: int,
    ):
        return (
            db.query(CartItem)
            .filter(CartItem.user_id == user_id)
            .all()
        )

    def get_cart_items_with_products(
        self,
        db: Session,
        user_id: int,
    ):
        return (
            db.query(CartItem)
            .options(joinedload(CartItem.product))
            .filter(CartItem.user_id == user_id)
            .all()
        )

    def update_cart_item(
        self,
        db: Session,
        cart_item: CartItem,
        quantity: int,
    ):
        cart_item.quantity = quantity

        db.commit()
        db.refresh(cart_item)

        return cart_item

    def delete_cart_item(
        self,
        db: Session,
        cart_item: CartItem,
    ):
        db.delete(cart_item)
        db.commit()

        return True

    def delete_cart_items_by_user(
        self,
        db: Session,
        user_id: int,
    ):
        cart_items = self.get_cart_items_by_user(db, user_id)

        for cart_item in cart_items:
            db.delete(cart_item)

        db.commit()

        return True
