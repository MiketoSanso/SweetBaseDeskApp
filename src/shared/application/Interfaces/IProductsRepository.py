from abc import ABC, abstractmethod
 

from src.features.products.domain.entities.Product import Product
from src.shared.infrastructure.Database import Database


class IProductsRepository(ABC):
    def __init__(self, db: Database):
        self.db = db

    @abstractmethod
    def get_products(self) -> list[Product]:
        pass

    @abstractmethod
    def add_product(self, product: Product):
        pass

    @abstractmethod
    def get_product_by_id(self, id: int) -> Product:
        pass

    @abstractmethod
    def delete_product(self, product_name: str):
        pass

    @abstractmethod
    def change_product_by_id(self, id: int, new_product: Product):
        pass
