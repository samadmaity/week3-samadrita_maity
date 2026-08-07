from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Category(Base):
    __tablename__="categories"

    category_id = Column(Integer, primary_key=True, index= True)
    category_name = Column(String(100), unique=True, nullable=False)
    products = relationship("Product", back_populates="category")
