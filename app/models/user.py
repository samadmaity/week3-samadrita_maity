from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key= True, index= True)
    name = Column(String(100), nullable= False)
    email = Column(String(100), unique= True, nullable= False)
    password = Column(String(255), nullable= False)
    mobile = Column(String(15), nullable= False)
    cart_items = relationship("CartItem",back_populates="user",cascade="all, delete-orphan")
    orders = relationship("Order",back_populates="user",cascade="all, delete-orphan")

