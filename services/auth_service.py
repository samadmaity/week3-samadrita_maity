from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repositories.user_repository import UserRepository
from utils.auth import create_access_token, verify_password
from utils.logger import logger

class AuthService:

    def __init__(self):

        self.user_repository = UserRepository()

    def login_user(
        self,
        db: Session,
        email: str,
        password: str,
    ):

        normalized_email = email.strip().lower()
        logger.info(
            "Login attempt for email=%s",
            normalized_email,
        )

        user = (
            self.user_repository.get_user_by_email(
                db,
                normalized_email,
            )
        )

        if user is None:
            logger.warning(
                "Login failed: user not found for email=%s",
                normalized_email,
            )

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={
                    "WWW-Authenticate": "Bearer",
                },
            )

        password_is_valid = verify_password(
            password,
            user.password,
        )

        if not password_is_valid:

            logger.warning(
                "Login failed: invalid password for email=%s",
                normalized_email,
            )

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={
                    "WWW-Authenticate": "Bearer",
                },
            )

        logger.info(
            "Successful login for user_id=%s",
            user.user_id,
        )

        access_token = create_access_token(
            data={
                "sub": user.email,
                "role": user.role,
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
