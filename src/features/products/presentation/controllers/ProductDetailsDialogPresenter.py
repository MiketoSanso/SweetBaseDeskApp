from src.features.ingredients.application.usecases.GetIngredientByIdUseCase import (
    GetIngredientByIDUseCase,
)
from src.features.products.application.dtos.IngredientDisplayDTO import (
    IngredientDisplayDTO,
)
from src.features.products.application.interfaces.IProductDetailsDialog import (
    IProductDetailsDialog,
)
from src.features.products.application.usecases.GetStockItemsUseCase import (
    GetStockItemsUseCase,
)
from src.features.products.domain.entities.Product import Product
from src.shared.application.Interfaces.IMessageService import IMessageService


class ProductDetailsDialogPresenter:
    def __init__(
        self,
        view: IProductDetailsDialog,
        message_service: IMessageService,
        get_ingredient_by_id_usecase: GetIngredientByIDUseCase,
        get_stock_items_usecase: GetStockItemsUseCase,
        product: Product,
    ):
        self.view = view
        self.message_service = message_service
        self.get_ingredient_by_id_usecase = get_ingredient_by_id_usecase
        self.get_stock_items_usecase = get_stock_items_usecase

        self.product = product

        self.set_ingredients_info()
        self.set_branches_info()

    def set_branches_info(self):
        self.view.set_product(self.product.name)

        stock_items = self.get_stock_items_usecase.execute(self.product.local_id)

        self.view.display_stock(stock_items.data)

    def set_ingredients_info(self):
        ingredients = [
            self.get_ingredient_by_id_usecase.execute(ingredient.ingredient_id).data
            for ingredient in self.product.ingredients
        ]

        total_cost = 0
        display_ingredients = []
        for i, ingredient in enumerate(ingredients):
            display_ingredients.append(
                IngredientDisplayDTO(
                    name=ingredient.name,
                    unit=ingredient.unit,
                    unit_cost=ingredient.unit_cost,
                    quantity=self.product.ingredients[i].quantity,
                )
            )

            total_cost += ingredient.unit_cost * self.product.ingredients[i].quantity

        self.view.display_ingredients(display_ingredients, total_cost)
