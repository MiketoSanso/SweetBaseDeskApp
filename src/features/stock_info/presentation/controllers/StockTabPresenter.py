from src.features.branches.application.usecases.GetBranchesUseCase import (
    GetBranchesUseCase,
)
from src.features.stock_info.application.interfaces.IStockTab import IStockTab
from src.features.stock_info.application.usecases.LoadStockItemsUseCase import (
    LoadStockItemsUseCase,
)
from src.features.stock_info.presentation.controllers.StockDialogPresenter import (
    StockDialogPresenter,
)
from src.features.stock_info.presentation.PQ.dialogs.StockDialog import StockDialog
from src.features.transactions.application.usecases.GetWarehousesUseCase import (
    GetWarehousesUseCase,
)
from src.shared.application.Interfaces.IMessageService import IMessageService


class StockTabPresenter:
    def __init__(
        self,
        view: IStockTab,
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

        self.view.set_on_open_stock_dialog_requested(
            self.on_open_stock_dialog_requested
        )

    def on_open_stock_dialog_requested(self):
        dialog = StockDialog()

        presenter = StockDialogPresenter(
            view=dialog,
            message_service=self.message_service,
            get_branches_usecase=self.get_branches_usecase,
            get_warehouses_usecase=self.get_warehouses_usecase,
            load_stock_items_usecase=self.load_stock_items_usecase,
        )

        dialog.exec()
