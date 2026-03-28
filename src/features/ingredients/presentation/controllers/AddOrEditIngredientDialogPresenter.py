import logging
from typing import Callable

from src.features.ingredients.application.dtos.IngredientCreateDTO import (
    IngredientCreateDTO,
)
from src.features.ingredients.application.interfaces.IAddIngredientDialog import (
    IAddIngredientDialog,
)
from src.features.ingredients.application.usecases.AddIngredientUseCase import (
    AddIngredientUseCase,
)
from src.features.ingredients.application.usecases.EditIngredientUseCase import (
    EditIngredientUseCase,
)
from src.features.ingredients.domain.entities.Ingredient import Ingredient
from src.shared.application.Interfaces.IMessageService import IMessageService


class AddOrEditIngredientDialogPresenter:
    def __init__(
        self,
        view: IAddIngredientDialog,
        message_service: IMessageService,
        add_ingredient_usecase: AddIngredientUseCase | None = None,
        edit_ingredient_usecase: EditIngredientUseCase | None = None,
        ingredient_data: Ingredient | None = None,
    ):
        self.view = view
        self.message_service = message_service
        self.add_ingredient_usecase = add_ingredient_usecase
        self.edit_ingredient_usecase = edit_ingredient_usecase
        self.ingredient_data = ingredient_data

        self._success_callbacks = []

        self.view.set_on_ingredient_data_entered(self._on_ingredient_data_entered)

        self._update_text()

    def _update_text(self):
        if self.edit_ingredient_usecase:
            if self.ingredient_data is not None:
                self.view.set_data(self.ingredient_data)
            else:
                logger = logging.getLogger(__name__)
                logger.exception(
                    f"Exception in AddOrEditIngredientDialogPresenter: self.id_editing_ingredient is None!"
                )
                return

    def _on_ingredient_data_entered(self, data: dict):
        ingredient_dto = IngredientCreateDTO(
            name=data["name"],
            unit=data["unit"],
            unit_cost=data["unit_cost"],
            description=data["description"],
        )

        if self.edit_ingredient_usecase and self.ingredient_data.local_id is not None:
            process_dto = self.edit_ingredient_usecase.execute(
                self.ingredient_data.local_id, ingredient_dto
            )
        elif self.add_ingredient_usecase:
            process_dto = self.add_ingredient_usecase.execute(ingredient_dto)
        else:
            logger = logging.getLogger(__name__)
            logger.exception(
                f"Exception in AddOrEditIngredientDialogPresenter: self.id_editing_ingredient is None!"
            )
            return

        if process_dto.status:
            self.message_service.show_success("Успех", process_dto.message, self.view)
            self.view.close_dialog()

            for callback in self._success_callbacks:
                callback()
        else:
            self.message_service.show_error("Ошибка", process_dto.message, self.view)

    def set_on_success_callback(self, callback: Callable[[], None]):
        self._success_callbacks.append(callback)
