import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from pathlib import Path


config_file = Path(__file__).resolve().parents[1] / "config.env"

load_dotenv(config_file)


SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is missing from the .env file")


ALGORITHM = os.getenv("ALGORITHM", "HS256")
TOKEN_EXPIRE_MINUTES = int(
    os.getenv("TOKEN_EXPIRE_MINUTES", "20")
)


password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)



oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login",
)


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    try:
        return password_context.verify(
            plain_password,
            hashed_password,
        )
    except (ValueError, TypeError):
        return False


def create_access_token(data: dict) -> str:
    token_data = data.copy()

    expiry_time = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=TOKEN_EXPIRE_MINUTES
    )

    token_data.update(
        {
            "exp": expiry_time,
        }
    )

    return jwt.encode(
        token_data,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        email = payload.get("sub")

        if not isinstance(email, str) or not email:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = (
        db.query(User)
        .filter(User.email == email.strip().lower())
        .first()
    )

    if user is None:
        raise credentials_exception

    return user


def require_roles(*allowed_roles: str):
    def role_dependency(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient role permissions",
            )

        return current_user

    return role_dependency
