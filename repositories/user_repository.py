from sqlalchemy.orm import Session
from app.models.user import User
from schemas.user_schema import UserCreate

class UserRepository:

    def create_user(self, db: Session, user: UserCreate):

        new_user= User(
            name= user.name,
            email= user.email,
            password= user.password,
            mobile= user.mobile
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    def get_user_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def login_user(self, db: Session, email: str, password: str):
        return db.query(User).filter(
            User.email == email,
            User.password == password
        ).first()