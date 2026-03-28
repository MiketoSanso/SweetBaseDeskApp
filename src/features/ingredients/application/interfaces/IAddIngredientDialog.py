from abc import ABC, abstractmethod
from typing import Callable

from src.features.ingredients.domain.entities.Ingredient import Ingredient


class IAddIngredientDialog(ABC):
    @abstractmethod
    def set_on_ingredient_data_entered(self, callback: Callable[[dict], None]):
        pass

    @abstractmethod
    def set_data(self, ingredient: Ingredient):
        pass

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def close_dialog(self):
        pass
