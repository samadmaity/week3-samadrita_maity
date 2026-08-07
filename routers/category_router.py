from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database import get_db
from schemas.category_schema import CategoryCreate, CategoryResponse
from services.category_service import CategoryService

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

category_service= CategoryService()

@router.post("/", response_model=CategoryResponse)

def create_category(category: CategoryCreate, db:Session = Depends(get_db)):
    return category_service.create_category(db,category)

@router.get("/",response_model=List[CategoryResponse])

def get_all_categories(db: Session= Depends(get_db)):
    return category_service.get_all_categories(db)