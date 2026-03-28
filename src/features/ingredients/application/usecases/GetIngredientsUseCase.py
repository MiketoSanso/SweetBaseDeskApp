from src.shared.application.dtos.ProcessDTO import ProcessDTO
from src.shared.application.usecases.Decorators.BaseUseCaseDecorator import usecase_func
from src.shared.infrastructure.repositories.IngredientsRepository import (
    IngredientsRepository,
)


class GetIngredientsUseCase:
    def __init__(self, db: IngredientsRepository):
        self.db = db

    @usecase_func
    def execute(self) -> ProcessDTO:
        ingredients = self.db.get_ingredients()

        if not ingredients:
            return ProcessDTO(
                status=False,
                message="Ингредиентов нет!",
                error="Repository returned None",
            )

        return ProcessDTO(
            status=True, message="Ингредиенты отправлены.", data=ingredients
        )
