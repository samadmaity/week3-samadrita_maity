from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from schemas.order_schema import OrderCreate, OrderResponse
from services.order_service import OrderService
from utils.auth import get_current_user
from utils.notification import send_order_confirmation


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


order_service = OrderService()


@router.post(
    "/checkout",
    response_model=OrderResponse,
)
async def checkout(
    order_data: OrderCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = order_service.checkout(
        db,
        order_data,
        current_user.user_id,
    )

    background_tasks.add_task(
        send_order_confirmation,
        order.order_id,
        current_user.user_id,
        order.total_amount,
    )

    return order


@router.get(
    "/details/{order_id}",
    response_model=OrderResponse,
)
def get_order_details(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return order_service.get_order_details(
        db,
        order_id,
        current_user.user_id,
    )


@router.get(
    "/{user_id}",
    response_model=list[OrderResponse],
)
def get_order_history(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return order_service.get_order_history(
        db,
        user_id,
        current_user.user_id,
    )
