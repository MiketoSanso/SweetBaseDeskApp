import pytest

from src.features.ingredients.application.dtos.IngredientCreateDTO import (
    IngredientCreateDTO,
)
from src.features.ingredients.application.usecases.AddIngredientUseCase import (
    AddIngredientUseCase,
)
from src.features.ingredients.application.usecases.DeleteIngredientUseCase import (
    DeleteIngredientUseCase,
)


class TestDeleteIngredientUseCase:
    @pytest.mark.parametrize(
        "id, count_usages, should_success",
        [(1, 0, True), (1, 1, False)],
    )
    def test_delete_ingredient(self, dependencies, id, count_usages, should_success):
        usecase: AddIngredientUseCase = dependencies.add_ingredient_usecase
        dto_add = IngredientCreateDTO(
            name="Имя", unit="10 шт.", unit_cost=10, description="description"
        )
        result = usecase.execute(dto_add)

        assert result.status

        ingredient_repo = dependencies.ingredients_repo
        if count_usages > 0:
            ingredient_repo.increment_usage(id)

        usecase: DeleteIngredientUseCase = dependencies.delete_ingredient_usecase
        result = usecase.execute(id)

        assert result.status is should_success
