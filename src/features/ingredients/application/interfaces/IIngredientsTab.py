from abc import ABC, abstractmethod
from typing import Callable


class IIngredientsTab(ABC):
    @abstractmethod
    def set_on_manage_ingredients_requested(self, callback: Callable[[], None]):
        pass

    @abstractmethod
    def update_stats(self, count):
        pass
