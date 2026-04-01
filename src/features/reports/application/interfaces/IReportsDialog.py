from abc import ABC, abstractmethod
from typing import Callable

from src.shared.application.dtos.ObjectDisplayDTO import ObjectDisplayDTO


class IReportsDialog(ABC):
    @abstractmethod
    def set_on_filters_changed(self, callback: Callable[[dict], None]):
        pass

    @abstractmethod
    def set_on_branch_changed(self, callback: Callable[[int], None]):
        pass

    @abstractmethod
    def set_branches(self, branches, has_branches):
        pass

    @abstractmethod
    def set_warehouses(self, warehouses: list[ObjectDisplayDTO]):
        pass

    @abstractmethod
    def display_transactions(self, transactions):
        pass

    @abstractmethod
    def close_dialog(self):
        pass
