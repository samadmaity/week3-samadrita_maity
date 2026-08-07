
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CartItemCreate(BaseModel):
    user_id: int = Field(
        ...,
        gt=0,
    )

    product_id: int = Field(
        ...,
        gt=0,
    )

    quantity: int = Field(
        ...,
        gt=0,
    )


class CartItemUpdate(BaseModel):
    quantity: int = Field(
        ...,
        gt=0,
    )


class CartItemResponse(BaseModel):
    cart_item_id: int
    user_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes= True


class CartSummaryResponse(BaseModel):
    items: list[CartItemResponse]
    total_items: int
    total_quantity: int
    total_amount: Decimal
