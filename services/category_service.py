from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repositories.category_repository import CategoryRepository
from schemas.category_schema import CategoryCreate

class CategoryService:

    def __init__(self):
        self.category_repository = CategoryRepository()

    def create_category(self, db: Session, category: CategoryCreate):
        existing_category = self.category_repository.get_category_by_name(db, category.category_name)
        if existing_category:
            raise HTTPException(status_code=400, detail="Category already exists")
        return self.category_repository.create_category(db, category)

    def get_all_categories(self, db: Session):
        return self.category_repository.get_all_categories(db)