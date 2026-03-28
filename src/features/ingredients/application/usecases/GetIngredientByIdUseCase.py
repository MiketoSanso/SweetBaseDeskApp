from src.shared.application.dtos.ProcessDTO import ProcessDTO
from src.shared.application.usecases.Decorators.BaseUseCaseDecorator import usecase_func
from src.shared.infrastructure.repositories.IngredientsRepository import (
    IngredientsRepository,
)


class GetIngredientByIDUseCase:
    def __init__(self, db: IngredientsRepository):
        self.db = db

    @usecase_func
    def execute(self, id: int) -> ProcessDTO:
        ingredient = self.db.get_ingredient_by_id(id)

        if not ingredient:
            return ProcessDTO(
                status=False,
                message="Ингредиент не найден!",
                error="Ingredient not found!",
            )

        return ProcessDTO(
            status=True, message="Ингредиент успешно найден!", data=ingredient
        )
