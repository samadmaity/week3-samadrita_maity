from sqlalchemy.orm import Session

from repositories.user_repository import UserRepository
from fastapi import HTTPException, status
from schemas.user_schema import UserCreate, UserLogin
from utils.auth import hash_password



class UserService:

    def __init__(self):
        self.user_repository = UserRepository()

    

    def register_user(
        self,
        db: Session,
        user: UserCreate,
    ):

        normalized_email = str(
            user.email
        ).strip().lower()

        existing_user = (
            self.user_repository.get_user_by_email(
                db,
                normalized_email,
            )
        )

        if existing_user:

            raise HTTPException(
                status_code=400,
                detail="Email already exists",
            )

        hashed_password = hash_password(
            user.password
        )

        user_data = user.model_copy(
            update={
                "email": normalized_email,
                "password": hashed_password,
            }
        )

        return self.user_repository.create_user(
            db,
            user_data,
        )


    