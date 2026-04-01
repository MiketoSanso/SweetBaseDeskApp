from typing import Callable  

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
from src.features.products.application.dtos.ProductCreateDTO import ProductCreateDTO
from src.features.products.application.dtos.ProductIngredientDisplayDTO import (
    ProductIngredientDisplayDTO,
)
from src.features.products.application.interfaces.IAddProductDialog import (
    IAddProductDialog,
)
from src.features.products.application.usecases.AddProductUseCase import (
    AddProductUseCase,
)
from src.features.products.domain.value_objects.ProductIngredientVO import (
    ProductIngredientVO,
)
from src.shared.application.Interfaces.IMessageService import IMessageService


class AddProductDialogPresenter:
    def __init__(
        self,
        view: IAddProductDialog,
        message_service: IMessageService,
        add_product_usecase: AddProductUseCase,
        get_ingredients_usecase: GetIngredientsUseCase,
        get_data_ingredient_by_id: GetIngredientByIDUseCase,
    ):
        self.view = view
        self.message_service = message_service
        self.add_product_usecase = add_product_usecase
        self.get_ingredients_usecase = get_ingredients_usecase
        self.get_data_ingredient_by_id = get_data_ingredient_by_id

        self._success_callbacks = []
        self.product_ingredients: list[ProductIngredientDisplayDTO] = []
        self.tech_ingredients: list[ProductIngredientVO] = []

        self.view.set_on_save_product_requested(
            self.tech_ingredients, self.on_save_product_requested
        )
        self.view.set_on_add_ingredient_requested(self.on_add_ingredient_requested)
        self.view.set_on_remove_ingredient_requested(
            self.on_remove_ingredient_requested
        )

    def on_add_ingredient_requested(self):
        dialog = ManageIngredientsDialog()

        presenter = ManageIngredientsDialogPresenter(
            view=dialog,
            message_service=self.message_service,
            add_ingredient_usecase=None,
            get_ingredients_usecase=self.get_ingredients_usecase,
            delete_ingredient_usecase=None,
            edit_ingredient_usecase=None,
            get_data_ingredient_by_id_usecase=None,
            is_management=False,
        )

        presenter.set_on_ingredient_selected(self.add_ingredient_to_list)

        dialog.exec()

    def on_remove_ingredient_requested(self, id: int):
        for i, ingredient in enumerate(self.tech_ingredients):

            if ingredient.ingredient_id == id:
                self.product_ingredients.pop(i)
                self.tech_ingredients.pop(i)
                self.view.update_display(self.product_ingredients)
                return

    def on_save_product_requested(self, data):
        dto = ProductCreateDTO(name=data["name"], ingredients=data["ingredients"])

        result = self.add_product_usecase.execute(dto)

        if result.status:
            self.view.close_dialog()

            self.message_service.show_success("Успех", result.message, self.view)

            for callback in self._success_callbacks:
                callback()
        else:
            self.message_service.show_error("Ошибка", result.message, self.view)

    def add_ingredient_to_list(self, id: int, quantity: int):
        ingredient = self.get_data_ingredient_by_id.execute(id)

        if ingredient.data:
            view_ingredient = ProductIngredientDisplayDTO(
                id=ingredient.data.local_id,
                name=ingredient.data.name,
                quantity=quantity,
                unit=ingredient.data.unit,
                cost=ingredient.data.unit_cost,
            )

            tech_ingredient = ProductIngredientVO(
                ingredient_id=ingredient.data.local_id, quantity=quantity
            )

            self.product_ingredients.append(view_ingredient)
            self.tech_ingredients.append(tech_ingredient)

            self.view.update_display(self.product_ingredients)

    def set_on_success_callback(self, callback: Callable[[], None]):
        self._success_callbacks.append(callback)
