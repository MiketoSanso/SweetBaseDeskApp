from abc import ABC, abstractmethod
 

from src.features.ingredients.domain.entities.Ingredient import Ingredient
from src.shared.infrastructure.Database import Database


class IIngredientsRepository(ABC):
    def __init__(self, db: Database):
        self.db = db

    @abstractmethod
    def get_ingredients(self) -> list[Ingredient]:
        pass

    @abstractmethod
    def add_ingredient(self, ingredient: Ingredient):
        pass

    @abstractmethod
    def get_ingredient_by_id(self, id: int) -> Ingredient:
        pass

    @abstractmethod
    @abstractmethod
    def change_ingredient_by_id(self, new_ingredient: Ingredient, id: int):
        pass

    @abstractmethod
    def increment_usage(self, id: int):
        pass

    @abstractmethod
    def delete_ingredient(self, id: int) -> bool:
        pass
