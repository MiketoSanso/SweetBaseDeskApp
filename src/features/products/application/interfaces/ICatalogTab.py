from abc import ABC, abstractmethod
from typing import Callable


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
    def display_products(self, products, has_products):
        pass
