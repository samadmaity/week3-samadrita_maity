from sqlalchemy.orm import Session

from repositories.user_repository import UserRepository
from fastapi import HTTPException, status
from schemas.user_schema import UserCreate, UserLogin

class UserService:

    def __init__(self):
        self.user_repository = UserRepository()

    def register_user(self, db:Session, user: UserCreate):

        existing_user = self.user_repository.get_user_by_email(
            db,
            user.email
        )

        if existing_user:
            raise HTTPException(status_code=400, detail="Email already exists")

        return self.user_repository.create_user(db, user)

    def login_user(self, db:Session, user: UserLogin):

        existing_user = self.user_repository.login_user(
            db,
            user.email,
            user.password
        )

        if existing_user is None:
            raise HTTPException(status_code=401, detail="Invalid Email or password")

        return {"message": "Login Successful"}