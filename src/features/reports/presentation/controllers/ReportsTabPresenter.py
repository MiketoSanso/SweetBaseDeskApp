from src.features.branches.application.usecases.GetBranchesUseCase import (
    GetBranchesUseCase,
)
from src.features.reports.application.usecases.GetTransactionsByFiltersUseCase import (
    GetTransactionsByFiltersUseCase,
)
from src.features.reports.application.usecases.GetTransactionsInfoUseCase import (
    GetTransactionsInfoUseCase,
)
from src.features.reports.presentation.controllers.ReposrtDialogPresenter import (
    ReportsDialogPresenter,
)
from src.features.reports.presentation.PQ.dialogs.ReportsDialog import ReportsDialog
from src.features.reports.presentation.PQ.tabs.ReportsTab import ReportsTab
from src.features.transactions.application.usecases.GetWarehousesUseCase import (
    GetWarehousesUseCase,
)
from src.shared.application.Interfaces.IMessageService import IMessageService


class ReportsTabPresenter:
    def __init__(
        self,
        view: ReportsTab,
        message_service: IMessageService,
        get_transactions_info_usecase: GetTransactionsInfoUseCase,
        get_transactions_by_filters_usecase: GetTransactionsByFiltersUseCase,
        get_branches_usecase: GetBranchesUseCase,
        get_warehouses_usecase: GetWarehousesUseCase,
    ):
        self.view = view
        self.message_service = message_service
        self.get_transactions_info_usecase = get_transactions_info_usecase
        self.get_transactions_by_filters_usecase = get_transactions_by_filters_usecase
        self.get_branches_usecase = get_branches_usecase
        self.get_warehouses_usecase = get_warehouses_usecase

        self.view.set_on_open_reports_requested(self.on_open_reports_requested)

        self._display_transactions_info()

    def on_load_transactions_requested(self):
        self._display_transactions_info()

    def on_open_reports_requested(self):
        dialog = ReportsDialog()

        presenter = ReportsDialogPresenter(
            view=dialog,
            message_service=self.message_service,
            get_transactions_by_filters_usecase=self.get_transactions_by_filters_usecase,
            get_branches_usecase=self.get_branches_usecase,
            get_warehouses_usecase=self.get_warehouses_usecase,
        )

        dialog.exec()

    def _display_transactions_info(self):
        transactions_info = self.get_transactions_info_usecase.execute()

        self.view.display_stats(transactions_info.data)
