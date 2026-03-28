from abc import ABC, abstractmethod
from typing import Callable


class IStockTab(ABC):
    @abstractmethod
    def set_on_open_stock_dialog_requested(self, callback: Callable[[], None]):
        pass

    @abstractmethod
    def display_stats(self, branches_count, products_count):
        pass
