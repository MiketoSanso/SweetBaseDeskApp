 

from src.features.ingredients.domain.entities.Ingredient import Ingredient
from src.features.ingredients.infrastructure.models.IngredientORM import IngredientORM
from src.shared.application.Interfaces.IIngredientsRepository import (
    IIngredientsRepository,
)
from src.shared.infrastructure.Database import Database
from src.shared.infrastructure.repositories.Decorators.RepositoryDecorator import (
    repo_func,
)


class IngredientsRepository(IIngredientsRepository):
    def __init__(self, db: Database):
        super().__init__(db)

    @repo_func
    def get_ingredients(self, session=None) -> list[Ingredient]:
        orm_ingredients = session.query(IngredientORM).all()
        ingredients = [
            Ingredient.model_validate(orm_ingredient)
            for orm_ingredient in orm_ingredients
        ]
        ingredients_list = [ingredient for ingredient in ingredients]
        return ingredients_list

    @repo_func
    def add_ingredient(self, ingredient: Ingredient, session=None):
        orm_ingredient = IngredientORM(**ingredient.model_dump())
        session.add(orm_ingredient)

    @repo_func
    def get_ingredient_by_id(self, id: int, session=None) -> Ingredient:
        orm_ingredient = session.get(IngredientORM, id)
        ingredient = Ingredient.model_validate(orm_ingredient)
        return ingredient

    @repo_func
    def change_ingredient_by_id(
        self, new_ingredient: Ingredient, id: int, session=None
    ):
        ingredient = session.get(IngredientORM, id)

        if ingredient:
            ingredient.name = new_ingredient.name
            ingredient.unit_cost = new_ingredient.unit_cost
            ingredient.unit = new_ingredient.unit
            ingredient.description = new_ingredient.description

    @repo_func
    def increment_usage(self, id: int, session=None):
        ingredient = session.get(IngredientORM, id)
        if ingredient:
            ingredient.count_usages += 1

    @repo_func
    def delete_ingredient(self, id: int, session=None):
        ingredient = session.get(IngredientORM, id)

        if ingredient is not None and ingredient.count_usages == 0:
            session.delete(ingredient)
