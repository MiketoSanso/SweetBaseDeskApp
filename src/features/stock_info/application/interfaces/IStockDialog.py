from abc import ABC, abstractmethod
from typing import Callable


class IStockDialog(ABC):
    @abstractmethod
    def set_on_branch_changed(self, callback: Callable[[int], None]):
        pass

    @abstractmethod
    def set_on_load_stock_requested(self, callback: Callable[[dict], None]):
        pass

    @abstractmethod
    def set_branches(self, branches, has_branches):
        pass

    @abstractmethod
    def set_warehouses(self, warehouses):
        pass

    @abstractmethod
    def display_stock(self, items, total_value):
        pass

    @abstractmethod
    def close_dialog(self):
        pass
