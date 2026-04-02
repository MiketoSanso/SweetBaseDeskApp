from src.features.products.application.dtos.StockItemDisplayDTO import (
    StockItemDisplayDTO,
)
from src.shared.application.dtos.ProcessDTO import ProcessDTO
from src.shared.application.Interfaces.IBranchesRepository import IBranchesRepository
from src.shared.application.Interfaces.IStockItemsRepository import (
    IStockItemsRepository,
)
from src.shared.application.usecases.Decorators.BaseUseCaseDecorator import usecase_func


class GetStockItemsUsecase:
    def __init__(
        self, stock_item_repo: IStockItemsRepository, branches_repo: IBranchesRepository
    ):
        self.stock_item_repo = stock_item_repo
        self.branches_repo = branches_repo

    @usecase_func
    def execute(self, product_id: int) -> ProcessDTO:
        stock_items = self.stock_item_repo.get_stock_items(product_id)

        if not stock_items:
            return ProcessDTO(
                status=False, message="Продуктов нет!", error="Repository returned None"
            )

        stock_display_items: list[StockItemDisplayDTO] = []

        for item in stock_items:
            branch = self.branches_repo.get_branch_by_id(item.branch_id)
            branch_name = branch.name
            warehouse_name = f"Склад {item.stock_id}"

            stock_item = StockItemDisplayDTO(
                branch_name=branch_name,
                warehouse_name=warehouse_name,
                quantity=item.quantity,
            )
            stock_display_items.append(stock_item)

        return ProcessDTO(
            status=True, message="Продукты отправлены.", data=stock_display_items
        )
