
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from schemas.order_schema import OrderCreate, OrderResponse
from services.order_service import OrderService


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


order_service = OrderService()


@router.post(
    "/checkout",
    response_model=OrderResponse,
)
def checkout(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
):

    return order_service.checkout(
        db,
        order_data,
    )


@router.get(
    "/details/{order_id}",
    response_model=OrderResponse,
)
def get_order_details(
    order_id: int,
    db: Session = Depends(get_db),
):

    return order_service.get_order_details(
        db,
        order_id,
    )


@router.get(
    "/{user_id}",
    response_model=list[OrderResponse],
)
def get_order_history(
    user_id: int,
    db: Session = Depends(get_db),
):

    return order_service.get_order_history(
        db,
        user_id,
    )
