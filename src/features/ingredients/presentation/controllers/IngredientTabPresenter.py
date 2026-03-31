from src.features.ingredients.application.interfaces.IIngredientsTab import (
    IIngredientsTab,
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
from src.features.ingredients.presentation.controllers.ManageIngredientsDialogPresenter import (
    ManageIngredientsDialogPresenter,
)
from src.features.ingredients.presentation.PQ.dialogs.ManageIngredientsDialog import (
    ManageIngredientsDialog,
)
from src.shared.application.Interfaces.IMessageService import IMessageService


class IngredientTabPresenter:
    def __init__(
        self,
        view: IIngredientsTab,
        message_service: IMessageService,
        add_ingredient_usecase: AddIngredientUseCase,
        get_ingredients_usecase: GetIngredientsUseCase,
        delete_ingredient_usecase: DeleteIngredientUseCase,
        edit_ingredient_usecase: EditIngredientUseCase,
        get_data_ingredient_by_id_usecase: GetIngredientByIDUseCase,
    ):
        self.view = view
        self.message_service = message_service
        self.add_ingredient_usecase = add_ingredient_usecase
        self.get_ingredients_usecase = get_ingredients_usecase
        self.delete_ingredient_usecase = delete_ingredient_usecase
        self.edit_ingredient_usecase = edit_ingredient_usecase
        self.get_data_ingredient_by_id_usecase = get_data_ingredient_by_id_usecase

        self.view.set_on_manage_ingredients_requested(
            self.on_manage_ingredients_requested
        )

    def on_manage_ingredients_requested(self):
        dialog = ManageIngredientsDialog()

        self._dialog_presenter = ManageIngredientsDialogPresenter(
            view=dialog,
            message_service=self.message_service,
            add_ingredient_usecase=self.add_ingredient_usecase,
            get_ingredients_usecase=self.get_ingredients_usecase,
            delete_ingredient_usecase=self.delete_ingredient_usecase,
            edit_ingredient_usecase=self.edit_ingredient_usecase,
            get_data_ingredient_by_id_usecase=self.get_data_ingredient_by_id_usecase,
            is_management=True,
        )

        dialog.exec()

    def update_stats(self, count):
        pass
