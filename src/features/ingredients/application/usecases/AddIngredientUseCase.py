from src.features.ingredients.application.dtos.IngredientCreateDTO import (
    IngredientCreateDTO,
)
from src.features.ingredients.domain.entities.Ingredient import Ingredient
from src.shared.application.dtos.ProcessDTO import ProcessDTO
from src.shared.application.usecases.Decorators.BaseUseCaseDecorator import usecase_func
from src.shared.infrastructure.repositories.IngredientsRepository import (
    IngredientsRepository,
)


class AddIngredientUseCase:
    def __init__(self, db: IngredientsRepository):
        self.db = db

    @usecase_func
    def execute(self, dto: IngredientCreateDTO) -> ProcessDTO:
        if not dto.name:
            return ProcessDTO(
                status=False,
                message="Имя ингредиента должно быть заполнено!",
                error="Ingredient name is not defined!",
            )

        if not dto.unit[0].isdigit() or dto.unit[0] == "0":
            return ProcessDTO(
                status=False,
                message="Некорректная единица измерения!",
                error="Ingredient unit is not correct!",
            )

        if dto.unit_cost <= 0:
            return ProcessDTO(
                status=False,
                message="Цена не может быть меньше 0 или равна 0!",
                error="Ingredient cost is not correct!",
            )

        ingredient = Ingredient.model_validate(dto)

        self.db.add_ingredient(ingredient)

        return ProcessDTO(status=True, message="Ингредиент успешно создан!")
