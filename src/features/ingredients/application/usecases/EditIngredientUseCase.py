from src.features.ingredients.application.dtos.IngredientCreateDTO import (
    IngredientCreateDTO,
)
from src.shared.application.dtos.ProcessDTO import ProcessDTO
from src.shared.application.usecases.Decorators.BaseUseCaseDecorator import usecase_func
from src.shared.infrastructure.repositories.IngredientsRepository import (
    IngredientsRepository,
)


class EditIngredientUseCase:
    def __init__(self, db: IngredientsRepository):
        self.db = db

    @usecase_func
    def execute(self, id: int, dto: IngredientCreateDTO) -> ProcessDTO:
        old_ingredient = self.db.get_ingredient_by_id(id)

        if not old_ingredient:
            return ProcessDTO(
                status=False, message="Неверный ID!", error="Ingredient is not found!"
            )

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

        if dto.unit_cost <= 0 or dto.unit_cost >= 1000000000:
            return ProcessDTO(
                status=False,
                message="Цена не может быть меньше 0, равна 0 или больше миллиарда!",
                error="Ingredient cost is not correct!",
            )

        updated_data = dto.model_dump(exclude_unset=True)
        updated_ingredient = old_ingredient.model_copy(update=updated_data)

        self.db.change_ingredient_by_id(updated_ingredient, id)

        return ProcessDTO(status=True, message="Ингредиент изменен.")
