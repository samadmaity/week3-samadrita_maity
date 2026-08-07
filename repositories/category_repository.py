from sqlalchemy.orm import Session

from app.models.category import Category
from schemas.category_schema import CategoryCreate

class CategoryRepository:

    def create_category(self, db: Session, category: CategoryCreate):

        new_category = Category(category_name = category.category_name)

        db.add(new_category)
        db.commit()
        db.refresh(new_category)

        return new_category

    def get_category_by_name(self, db: Session, category_name: str):
        return db.query(Category).filter(Category.category_name == category_name).first()

    def get_all_categories(self, db: Session):
        return db.query(Category).all()