
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from schemas.cart_schema import (
    CartItemCreate,
    CartItemResponse,
    CartItemUpdate,
    CartSummaryResponse,
)
from services.cart_service import CartService


router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)


cart_service = CartService()


@router.post(
    "/add",
    response_model=CartItemResponse,
)
def add_cart_item(
    cart_item: CartItemCreate,
    db: Session = Depends(get_db),
):

    return cart_service.add_cart_item(
        db,
        cart_item,
    )


@router.get(
    "/{user_id}/summary",
    response_model=CartSummaryResponse,
)
def get_cart_summary(
    user_id: int,
    db: Session = Depends(get_db),
):

    return cart_service.get_cart_summary(
        db,
        user_id,
    )


@router.get(
    "/{user_id}",
    response_model=list[CartItemResponse],
)
def get_cart(
    user_id: int,
    db: Session = Depends(get_db),
):

    return cart_service.get_cart(
        db,
        user_id,
    )


@router.put(
    "/update/{cart_item_id}",
    response_model=CartItemResponse,
)
def update_cart_item(
    cart_item_id: int,
    cart_item_data: CartItemUpdate,
    db: Session = Depends(get_db),
):

    return cart_service.update_cart_item(
        db,
        cart_item_id,
        cart_item_data,
    )


@router.delete(
    "/remove/{cart_item_id}",
)
def remove_cart_item(
    cart_item_id: int,
    db: Session = Depends(get_db),
):

    return cart_service.remove_cart_item(
        db,
        cart_item_id,
    )
