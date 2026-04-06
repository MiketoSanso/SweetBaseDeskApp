import pytest

from src.features.ingredients.application.dtos.IngredientCreateDTO import (
    IngredientCreateDTO,
)
from src.features.ingredients.application.usecases.AddIngredientUseCase import (
    AddIngredientUseCase,
)


class TestAddIngredientUseCase:
    @pytest.mark.parametrize(
        "name, unit, unit_cost, description, should_success",
        [
            ("Имя", "10 шт.", 10, "описание", True),
            ("Имя", "10 шт.", 10, "", True),
            ("", "10 шт.", 10, "описание", False),
            ("Имя", "шт.", 10, "описание", False),
            ("Имя", "0 шт.", 10, "описание", False),
            ("Имя", "-1 шт.", 10, "описание", False),
            ("Имя", "10 шт.", 0, "описание", False),
            ("Имя", "10 шт.", -10, "описание", False),
            ("Имя", "10 шт.", 9999999999999, "описание", False),
        ],
    )
    def test_add_ingredient(
        self,
        dependencies,
        name,
        unit,
        unit_cost,
        description,
        should_success,
    ):
        usecase: AddIngredientUseCase = dependencies.add_ingredient_usecase
        dto = IngredientCreateDTO(
            name=name, unit=unit, unit_cost=unit_cost, description=description
        )

        result = usecase.execute(dto)

        assert result.status is should_success

        if should_success:
            all_ingredients = dependencies.ingredients_repo.get_ingredients()

            assert all_ingredients[0].name == name
            assert all_ingredients[0].unit == unit
            assert all_ingredients[0].unit_cost == unit_cost
            assert all_ingredients[0].description == description

    def test_add_multiple_ingredients(self, dependencies):
        usecase: AddIngredientUseCase = dependencies.add_ingredient_usecase
        usecase.execute(
            dto=IngredientCreateDTO(
                name="Имя 1", unit="1 шт", unit_cost=10, description="description"
            )
        )

        usecase.execute(
            dto=IngredientCreateDTO(
                name="Имя 2", unit="1 шт", unit_cost=10, description="description"
            )
        )

        usecase.execute(
            dto=IngredientCreateDTO(
                name="Имя 3", unit="1 шт", unit_cost=10, description="description"
            )
        )

        all_ingredients = dependencies.ingredients_repo.get_ingredients()
        names = [i.name for i in all_ingredients]

        assert len(names) == 3
        assert "Имя 1" in names
        assert "Имя 2" in names
        assert "Имя 3" in names
