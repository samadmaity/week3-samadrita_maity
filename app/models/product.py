
from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    product_name = Column(
        String(150),
        unique=True,
        nullable=False,
        index=True,
    )

    description = Column(
        Text,
        nullable=True,
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.category_id"),
        nullable=False,
        index=True,
    )

    price = Column(
        Numeric(10, 2),
        nullable=False,
    )

    available_quantity = Column(
        Integer,
        nullable=False,
        default=0,
    )

    product_url = Column(
        String(500),
        nullable=True,
    )

    category = relationship("Category", back_populates="products")
    cart_items = relationship("CartItem",back_populates="product")
    order_details = relationship("OrderDetail",back_populates="product")
