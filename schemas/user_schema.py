from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    email: EmailStr
    password: str = Field(..., min_length=6)
    mobile: str = Field(...,min_length=10,max_length=10)

class UserResponse(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    mobile: str
    role: str

    model_config = ConfigDict(
        from_attributes=True,
    )

class UserLogin(BaseModel):
    email: EmailStr
    password: str
