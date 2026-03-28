from typing import Callable

from src.features.ingredients.application.interfaces.IManageIngredientsDialog import (
    IManageIngredientsDialog,
)
from src.features.ingredients.application.usecases.AddIngredientUseCase import (
    AddIngredientUseCase,
)
from src.features.ingredients.application.usecases.DeleteIngredientUseCase import (
    DeleteIngredientUseCase,
)
from src.features.ingredients.application.usecases.EditIngredientUseCase import (
    EditIngredientUseCase,
)
from src.features.ingredients.application.usecases.GetIngredientByIdUseCase import (
    GetIngredientByIDUseCase,
)
from src.features.ingredients.application.usecases.GetIngredientsUseCase import (
    GetIngredientsUseCase,
)
from src.features.ingredients.presentation.controllers.AddOrEditIngredientDialogPresenter import (
    AddOrEditIngredientDialogPresenter,
)
from src.features.ingredients.presentation.PQ.dialogs.AddOrEditIngredientDialog import (
    AddOrEditIngredientDialog,
)
from src.shared.application.Interfaces.IMessageService import IMessageService


class ManageIngredientsDialogPresenter:
    def __init__(
        self,
        view: IManageIngredientsDialog,
        message_service: IMessageService,
        add_ingredient_usecase: AddIngredientUseCase | None,
        get_ingredients_usecase: GetIngredientsUseCase,
        delete_ingredient_usecase: DeleteIngredientUseCase | None,
        edit_ingredient_usecase: EditIngredientUseCase | None,
        get_data_ingredient_by_id_usecase: GetIngredientByIDUseCase | None,
        is_management: bool,
    ):
        self.view = view
        self.message_service = message_service
        self.add_ingredient_usecase = add_ingredient_usecase
        self.get_ingredients_usecase = get_ingredients_usecase
        self.delete_ingredient_usecase = delete_ingredient_usecase
        self.edit_ingredient_usecase = edit_ingredient_usecase
        self.get_data_ingredient_by_id_usecase = get_data_ingredient_by_id_usecase

        self._display_ingredients()

        self.view.set_on_add_ingredient_requested(self.on_add_ingredient_requested)
        self.view.set_on_delete_ingredient_requested(
            self.on_delete_ingredient_requested
        )
        self.view.set_on_edit_ingredient_requested(self.on_edit_ingredient_requested)

        if is_management:
            self.view.set_mode_management()
        else:
            self.view.set_mode_selection()

    def on_add_ingredient_requested(self):
        dialog = AddOrEditIngredientDialog()

        presenter = AddOrEditIngredientDialogPresenter(
            view=dialog,
            message_service=self.message_service,
            add_ingredient_usecase=self.add_ingredient_usecase,
        )

        presenter.set_on_success_callback(self._display_ingredients)

        dialog.exec()

    def set_on_ingredient_selected(self, callback: Callable[[int, int], None]):
        self.view.set_on_ingredient_selected(callback)

    def on_edit_ingredient_requested(self, id: int):
        dialog = AddOrEditIngredientDialog()

        ingredient = self.get_data_ingredient_by_id_usecase.execute(id)

        presenter = AddOrEditIngredientDialogPresenter(
            view=dialog,
            message_service=self.message_service,
            edit_ingredient_usecase=self.edit_ingredient_usecase,
            ingredient_data=ingredient.data,
        )

        presenter.set_on_success_callback(self._display_ingredients)

        dialog.exec()

    def on_delete_ingredient_requested(self, id: int):
        answer = self.message_service.show_question(
            "Удаление ингредиента",
            "Вы действительно хотите удалить ингредиент?",
            self.view,
        )

        if answer:
            result_dto = self.delete_ingredient_usecase.execute(id)

            if result_dto.status:
                self.message_service.show_success(
                    "Успех", result_dto.message, self.view
                )

                self._display_ingredients()
            else:
                self.message_service.show_error("Ошибка", result_dto.message, self.view)

    def _display_ingredients(self):
        ingredients_dto = self.get_ingredients_usecase.execute()
        self.view.display_ingredients(ingredients_dto.data, ingredients_dto.status)
