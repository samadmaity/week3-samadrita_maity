from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., min_lenghth=6)
    mobile: str = Field(...,min_length=10,max_length=10)

class UserResponse(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    mobile: str

    class Config:
        from_attributes= True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
