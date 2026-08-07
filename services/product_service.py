
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from repositories.product_repository import ProductRepository
from schemas.product_schema import ProductCreate, ProductUpdate
from app.models.category import Category


class ProductService:

    def __init__(self):
        self.product_repository = ProductRepository()

    def create_product(
        self,
        db: Session,
        product: ProductCreate,
    ):
        existing_product = self.product_repository.get_product_by_name(
            db,
            product.product_name,
        )

        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product name already exists",
            )

        category = db.query(Category).filter(
            Category.category_id == product.category_id
        ).first()

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        return self.product_repository.create_product(
            db,
            product,
        )

    def get_all_products(
        self,
        db: Session,
    ):
        return self.product_repository.get_all_products(db)

    def get_product_by_id(
        self,
        db: Session,
        product_id: int,
    ):
        product = self.product_repository.get_product_by_id(
            db,
            product_id,
        )

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        return product

    def search_products(
        self,
        db: Session,
        name: str | None = None,
        category_id: int | None = None,
    ):
        return self.product_repository.search_products(
            db,
            name,
            category_id,
        )

    def update_product(
        self,
        db: Session,
        product_id: int,
        product_data: ProductUpdate,
    ):
        product = self.product_repository.get_product_by_id(
            db,
            product_id,
        )

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        if (
            product_data.product_name
            and product_data.product_name != product.product_name
        ):
            existing_product = (
                self.product_repository.get_product_by_name(
                    db,
                    product_data.product_name,
                )
            )

            if existing_product:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Product name already exists",
                )

        if product_data.category_id is not None:
            category = db.query(Category).filter(
                Category.category_id == product_data.category_id
            ).first()

            if category is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Category not found",
                )

        return self.product_repository.update_product(
            db,
            product,
            product_data,
        )

    def delete_product(
        self,
        db: Session,
        product_id: int,
    ):
        product = self.product_repository.get_product_by_id(
            db,
            product_id,
        )

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        self.product_repository.delete_product(
            db,
            product,
        )

        return {
            "message": "Product deleted successfully",
        }
