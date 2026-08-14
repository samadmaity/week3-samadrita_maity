from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from schemas.auth_schema import Token
from schemas.user_schema import UserResponse
from services.auth_service import AuthService
from utils.auth import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


auth_service = AuthService()


@router.post(
    "/login",
    response_model=Token,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    return auth_service.login_user(
        db,
        form_data.username,
        form_data.password,
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_my_profile(
    current_user: User = Depends(get_current_user),
):

    return current_user
