from abc import ABC, abstractmethod
from typing import Callable


class IAddProductDialog(ABC):
    @abstractmethod
    def set_on_add_ingredient_requested(self, callback: Callable[[], None]):
        pass

    @abstractmethod
    def set_on_save_product_requested(
        self, ingredients: list, callback: Callable[[dict], None]
    ):
        pass

    @abstractmethod
    def set_on_remove_ingredient_requested(self, callback: Callable[[int], None]):
        pass

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def update_display(self, ingredients: list):
        pass

    @abstractmethod
    def close_dialog(self):
        pass
