import logging

from src.shared.application.dtos.ProcessDTO import ProcessDTO
from src.shared.application.usecases.Decorators.BaseUseCaseDecorator import usecase_func
from src.shared.infrastructure.repositories.IngredientsRepository import (
    IngredientsRepository,
)


class DeleteIngredientUseCase:
    def __init__(self, repo: IngredientsRepository):
        self.repo = repo

    @usecase_func
    def execute(self, id: int) -> ProcessDTO:
        try:
            ingredient = self.repo.get_ingredient_by_id(id)

            if ingredient.count_usages > 0:
                return ProcessDTO(
                    status=False,
                    message="Нельзя удалить ингредиент, который используется в продуктах!",
                    error="Value exception: ingredient is used in products!",
                )

            self.repo.delete_ingredient(id)

            return ProcessDTO(status=True, message="Ингредиент удалён!")
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(f"Exception in GetIngredientsUseCase")
            return ProcessDTO(
                status=False,
                message="Ошибка при загрузке ингредиентов!",
                error=f"Load db : {e}",
            )
