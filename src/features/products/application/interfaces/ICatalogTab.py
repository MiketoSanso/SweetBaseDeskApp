from abc import ABC, abstractmethod
from typing import Callable  

from src.features.products.application.dtos.ProductDisplayDTO import ProductDisplayDTO


class ICatalogTab(ABC):
    @abstractmethod
    def set_on_add_product_requested(self, callback: Callable[[], None]):
        pass

    @abstractmethod
    def set_on_refresh_catalog_requested(self, callback: Callable[[], None]):
        pass

    @abstractmethod
    def set_on_product_selected(self, callback: Callable[[int], None]):
        pass

    @abstractmethod
    def display_products(self, products: tuple[ProductDisplayDTO], has_products):
        pass
