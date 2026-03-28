from abc import ABC, abstractmethod


class IProductDetailsDialog(ABC):
    @abstractmethod
    def set_product(self, product_name):
        pass

    @abstractmethod
    def display_stock(self, stock_items):
        pass

    @abstractmethod
    def display_ingredients(self, ingredients, total_cost):
        pass

    @abstractmethod
    def close_dialog(self):
        pass
