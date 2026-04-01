from abc import ABC, abstractmethod
from typing import Callable  

from src.features.transactions.application.value_objects.TransactionItem import (
    TransactionItem,
)


class ITransactionTab(ABC):
    @abstractmethod
    def set_on_add_items_requested(self, callback: Callable[[], None]):
        pass

    @abstractmethod
    def set_on_process_transaction_requested(self, callback: Callable[[dict], None]):
        pass

    @abstractmethod
    def set_on_change_branch_requested(self, callback: Callable[[int], None]):
        pass

    @abstractmethod
    def set_branches(self, branches, has_branches):
        pass

    @abstractmethod
    def set_warehouses(self, warehouses):
        pass

    @abstractmethod
    def update_display(self, items: list[TransactionItem]):
        pass
