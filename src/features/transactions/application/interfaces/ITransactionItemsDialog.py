from abc import ABC, abstractmethod
from typing import Callable


class ITransactionItemsDialog(ABC):
    @abstractmethod
    def set_on_items_confirmed(self, callback: Callable[[], None]):
        pass

    @abstractmethod
    def set_on_add_item_requested(self, callback: Callable[[dict], None]):
        pass

    @abstractmethod
    def set_on_remove_item_requested(self, callback: Callable[[int], None]):
        pass

    @abstractmethod
    def set_products(self, products):
        pass

    @abstractmethod
    def update_table(self, items):
        pass

    @abstractmethod
    def close_dialog(self):
        pass
