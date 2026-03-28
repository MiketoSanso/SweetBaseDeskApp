from src.features.branches.application.usecases.GetBranchesUseCase import (
    GetBranchesUseCase,
)
from src.features.reports.application.dtos.TransactionFiltersDTO import (
    TransactionFiltersDTO,
)
from src.features.reports.application.interfaces.IReportsDialog import IReportsDialog
from src.features.reports.application.usecases.GetTransactionsByFiltersUseCase import (
    GetTransactionsByFiltersUseCase,
)
from src.features.transactions.application.usecases.GetWarehousesUseCase import (
    GetWarehousesUseCase,
)
from src.shared.application.Interfaces.IMessageService import IMessageService


class ReportsDialogPresenter:
    def __init__(
        self,
        view: IReportsDialog,
        message_service: IMessageService,
        get_transactions_by_filters_usecase: GetTransactionsByFiltersUseCase,
        get_branches_usecase: GetBranchesUseCase,
        get_warehouses_usecase: GetWarehousesUseCase,
    ):
        self.view = view
        self.message_service = message_service
        self.get_transactions_by_filters_usecase = get_transactions_by_filters_usecase
        self.get_branches_usecase = get_branches_usecase
        self.get_warehouses_usecase = get_warehouses_usecase

        self.view.set_on_filters_changed(self.on_filters_changed)
        self.view.set_on_branch_changed(self.on_branch_changed)

        self.set_data()

    def set_data(self):
        branches = self.get_branches_usecase.execute()

        if branches:
            self.view.set_branches(branches.data, branches.status)
            self.set_warehouses(1)

    def set_warehouses(self, id: int):
        warehouses = self.get_warehouses_usecase.execute(id)

        if warehouses.status:
            self.view.set_warehouses(warehouses.data)

    def on_filters_changed(self, data: dict):
        transaction_filters_dto = TransactionFiltersDTO(
            is_arrival=data["type"],
            branch_id=data["branch_id"],
            warehouse_id=data["warehouse_id"],
            date_from=data["date_from"],
            date_to=data["date_to"],
        )

        result = self.get_transactions_by_filters_usecase.execute(
            transaction_filters_dto
        )

        if result.status:
            self.view.display_transactions(result.data)

    def on_branch_changed(self, id: int):
        self.set_warehouses(id)
