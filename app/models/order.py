from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.database import Base


class Order(Base):

    __tablename__ = "orders"

    order_id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False,
        index=True,
    )

    order_date = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    payment_method = Column(
        String(50),
        nullable=False,
    )

    total_amount = Column(
        Numeric(10, 2),
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="orders",
    )

    order_details = relationship(
        "OrderDetail",
        back_populates="order",
        cascade="all, delete-orphan",
    )


class OrderDetail(Base):

    __tablename__ = "order_details"

    order_detail_id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.order_id"),
        nullable=False,
        index=True,
    )

    product_id = Column(
        Integer,
        ForeignKey("products.product_id"),
        nullable=False,
        index=True,
    )

    quantity = Column(
        Integer,
        nullable=False,
    )

    price = Column(
        Numeric(10, 2),
        nullable=False,
    )

    order = relationship(
        "Order",
        back_populates="order_details",
    )

    product = relationship(
        "Product",
        back_populates="order_details",
    )
