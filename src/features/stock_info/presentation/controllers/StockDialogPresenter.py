from src.features.branches.application.usecases.GetBranchesUseCase import (
    GetBranchesUseCase,
)
from src.features.stock_info.application.interfaces.IStockDialog import IStockDialog
from src.features.stock_info.application.usecases.LoadStockItemsUseCase import (
    LoadStockItemsUseCase,
)
from src.features.transactions.application.usecases.GetWarehousesUseCase import (
    GetWarehousesUseCase,
)
from src.shared.application.Interfaces.IMessageService import IMessageService


class StockDialogPresenter:
    def __init__(
        self,
        view: IStockDialog,
        message_service: IMessageService,
        get_branches_usecase: GetBranchesUseCase,
        get_warehouses_usecase: GetWarehousesUseCase,
        load_stock_items_usecase: LoadStockItemsUseCase,
    ):
        self.view = view
        self.message_service = message_service
        self.get_branches_usecase = get_branches_usecase
        self.get_warehouses_usecase = get_warehouses_usecase
        self.load_stock_items_usecase = load_stock_items_usecase

        self.view.set_on_load_stock_requested(self.on_load_stock_requested)
        self.view.set_on_branch_changed(self.set_warehouses)

        self.set_branches()

    def set_branches(self):
        result = self.get_branches_usecase.execute()

        self.view.set_branches(result.data, result.status)

        if result.status:
            self.set_warehouses(1)

    def set_warehouses(self, id: int):
        result = self.get_warehouses_usecase.execute(id)

        if result.status:
            self.view.set_warehouses(result.data)

    def on_load_stock_requested(self, data: dict):
        items = self.load_stock_items_usecase.execute(
            data["branch_id"], data["warehouse_id"]
        )
        cost = 0

        if items.status:
            for item in items.data:
                cost += item.cost

            self.view.display_stock(items, cost)
        else:
            self.view.display_stock(None, cost)
