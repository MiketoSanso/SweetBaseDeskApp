from src.features.stock_info.application.DTOs.StockDisplayDTO import StockDisplayDTO
from src.shared.application.dtos.ProcessDTO import ProcessDTO
from src.shared.application.usecases.Decorators.BaseUseCaseDecorator import usecase_func
from src.shared.infrastructure.repositories.IngredientsRepository import (
    IngredientsRepository,
)
from src.shared.infrastructure.repositories.ProductsRepository import ProductsRepository
from src.shared.infrastructure.repositories.StockItemsRepository import (
    StockItemsRepository,
)


class LoadStockItemsUseCase:
    def __init__(
        self,
        stock_repo: StockItemsRepository,
        products_repo: ProductsRepository,
        ingredients_repo: IngredientsRepository,
    ):
        self.stock_repo = stock_repo
        self.products_repo = products_repo
        self.ingredients_repo = ingredients_repo

    @usecase_func
    def execute(self, branch_id: int, warehouse_id: int) -> ProcessDTO:
        items = self.stock_repo.get_items_in_stock(branch_id, warehouse_id)

        stock_display_items = []

        if items is None:
            return ProcessDTO(
                status=False, message="Item-ов нету!", error="Items not found!"
            )
        for item in items:
            product = self.products_repo.get_product_by_id(item.product_id)

            cost = 0

            for ingredient in product.ingredients:
                loaded_ingredient = self.ingredients_repo.get_ingredient_by_id(
                    ingredient.ingredient_id
                )
                cost += loaded_ingredient.unit_cost * ingredient.quantity

            stock_item = StockDisplayDTO(
                product_name=product.name, quantity=item.quantity, cost=cost
            )

            stock_display_items.append(stock_item)

        return ProcessDTO(
            status=True, message="Загрузка выполнена успешно!", data=stock_display_items
        )
