import pytest

from src.features.ingredients.application.dtos.IngredientCreateDTO import (
    IngredientCreateDTO,
)
from src.features.ingredients.application.usecases.AddIngredientUseCase import (
    AddIngredientUseCase,
)
from src.features.ingredients.application.usecases.EditIngredientUseCase import (
    EditIngredientUseCase,
)


class TestEditIngredientUseCase:
    @pytest.mark.parametrize(
        "id, name, unit, unit_cost, description, should_success",
        [
            (1, "Имя", "10 шт.", 10, "описание", True),
            (1, "Имя", "10 шт.", 10, "", True),
            (1, "", "10 шт.", 10, "описание", False),
            (1, "Имя", "шт.", 10, "описание", False),
            (1, "Имя", "0 шт.", 10, "описание", False),
            (1, "Имя", "-1 шт.", 10, "описание", False),
            (1, "Имя", "10 шт.", 0, "описание", False),
            (1, "Имя", "10 шт.", -10, "описание", False),
            (1, "Имя", "10 шт.", 9999999999999, "описание", False),
        ],
    )
    def test_edit_ingredient(
        self,
        dependencies,
        id,
        name,
        unit,
        unit_cost,
        description,
        should_success,
    ):
        usecase_add: AddIngredientUseCase = dependencies.add_ingredient_usecase
        dto_add = IngredientCreateDTO(
            name="Имя", unit="10 шт.", unit_cost=10, description="description"
        )
        result = usecase_add.execute(dto_add)

        assert result.status

        usecase: EditIngredientUseCase = dependencies.edit_ingredient_usecase
        dto = IngredientCreateDTO(
            name=name, unit=unit, unit_cost=unit_cost, description=description
        )

        result = usecase.execute(id, dto)

        assert result.status is should_success

        if should_success:
            all_ingredients = dependencies.ingredients_repo.get_ingredients()

            assert all_ingredients[0].name == name
            assert all_ingredients[0].unit == unit
            assert all_ingredients[0].unit_cost == unit_cost
            assert all_ingredients[0].description == description
