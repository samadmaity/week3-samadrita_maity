from decimal import Decimal

from sqlalchemy.orm import Session, selectinload

from app.models.order import Order, OrderDetail


class OrderRepository:

    def create_order(
        self,
        db: Session,
        user_id: int,
        payment_method: str,
        total_amount: Decimal,
    ):

        new_order = Order(
            user_id=user_id,
            payment_method=payment_method,
            total_amount=total_amount,
        )

        db.add(new_order)
        db.flush()

        return new_order

    def create_order_detail(
        self,
        db: Session,
        order_id: int,
        product_id: int,
        quantity: int,
        price: Decimal,
    ):

        new_order_detail = OrderDetail(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price=price,
        )

        db.add(new_order_detail)
        db.flush()

        return new_order_detail

    def get_order_by_id(
        self,
        db: Session,
        order_id: int,
    ):

        return (
            db.query(Order)
            .options(
                selectinload(Order.order_details),
            )
            .filter(Order.order_id == order_id)
            .first()
        )

    def get_orders_by_user(
        self,
        db: Session,
        user_id: int,
    ):

        return (
            db.query(Order)
            .options(
                selectinload(Order.order_details),
            )
            .filter(Order.user_id == user_id)
            .order_by(Order.order_date.desc())
            .all()
        )

    def commit(self, db: Session):

        db.commit()

    def rollback(self, db: Session):

        db.rollback()
