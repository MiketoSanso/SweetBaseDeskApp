 

from src.features.products.application.dtos.ProductDisplayDTO import ProductDisplayDTO
from src.features.products.domain.entities.Product import Product
from src.features.products.infrastructure.models.ProductORM import ProductORM
from src.shared.application.Interfaces.IProductsRepository import IProductsRepository
from src.shared.infrastructure.Database import Database
from src.shared.infrastructure.repositories.Decorators.RepositoryDecorator import (
    repo_func,
)


class ProductsRepository(IProductsRepository):
    def __init__(self, db: Database):
        super().__init__(db)

    @repo_func
    def get_products(self, session=None) -> list[Product]:
        orm_products = session.query(ProductORM).all()
        products = [Product.model_validate(orm_product) for orm_product in orm_products]
        products_list = [product for product in products]
        return products_list

    @repo_func
    def add_product(self, product: Product, session=None):
        orm_product = ProductORM(**product.model_dump())
        session.add(orm_product)

    @repo_func
    def get_product_by_id(self, id: int, session=None) -> Product | None:
        orm_product = session.get(ProductORM, id)

        if not orm_product:
            return None

        product = Product.model_validate(orm_product)
        return product

    @repo_func
    def delete_product(self, id: int, session=None):
        orm_product = session.get(ProductORM, id)

        if not orm_product:
            raise ValueError(f"Продукт с id {id} не найден")

        session.delete(orm_product)

    @repo_func
    def change_product_by_id(self, id: int, new_product: Product, session=None):
        orm_product = session.get(ProductORM, id)

        if orm_product:
            orm_product.name = new_product.name
            orm_product.image_path = new_product.image_path
            orm_product.ingredients = [
                ingredient.model_dump() for ingredient in new_product.ingredients
            ]
