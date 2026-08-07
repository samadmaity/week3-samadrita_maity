
from decimal import Decimal

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    product_name: str = Field(
        ...,
        min_length=2,
        max_length=150,
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
    )

    category_id: int = Field(
        ...,
        gt=0,
    )

    price: Decimal = Field(
        ...,
        gt=0,
    )

    available_quantity: int = Field(
        ...,
        ge=0,
    )

    product_url: str | None = Field(
        default=None,
        max_length=500,
    )


class ProductResponse(BaseModel):
    product_id: int
    product_name: str
    description: str | None
    category_id: int
    price: Decimal
    available_quantity: int
    product_url: str | None

    class Config:
        from_attributes = True


class ProductUpdate(BaseModel):
    product_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
    )

    category_id: int | None = Field(
        default=None,
        gt=0,
    )

    price: Decimal | None = Field(
        default=None,
        gt=0,
    )

    available_quantity: int | None = Field(
        default=None,
        ge=0,
    )

    product_url: str | None = Field(
        default=None,
        max_length=500,
    )
