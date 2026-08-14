from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class OrderCreate(BaseModel):
    payment_method: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )


class OrderDetailResponse(BaseModel):
    order_detail_id: int
    order_id: int
    product_id: int
    quantity: int
    price: Decimal

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    order_id: int
    user_id: int
    order_date: datetime
    payment_method: str
    total_amount: Decimal
    order_details: list[OrderDetailResponse] = Field(
        default_factory=list,
    )

    model_config = ConfigDict(from_attributes=True)

