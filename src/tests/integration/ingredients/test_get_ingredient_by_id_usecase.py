import pytest

from src.features.ingredients.application.dtos.IngredientCreateDTO import (
    IngredientCreateDTO,
)
from src.features.ingredients.application.usecases.AddIngredientUseCase import (
    AddIngredientUseCase,
)
from src.features.ingredients.application.usecases.GetIngredientByIdUseCase import (
    GetIngredientByIDUseCase,
)


class TestGetIngredientByIDUseCase:
    @pytest.mark.parametrize(
        "id, should_success",
        [(1, True), (-1, False), (9999999, False)],
    )
    def test_get_ingredient_by_id(self, dependencies, id, should_success):
        usecase: AddIngredientUseCase = dependencies.add_ingredient_usecase
        dto_add = IngredientCreateDTO(
            name="Имя", unit="10 шт.", unit_cost=10, description="description"
        )
        result = usecase.execute(dto_add)

        assert result.status

        usecase: GetIngredientByIDUseCase = (
            dependencies.get_data_ingredient_by_id_usecase
        )
        result = usecase.execute(id)

        assert result.status is should_success
