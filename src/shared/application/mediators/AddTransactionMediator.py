from src.features.products.presentation.controllers.ProductsTabPresenter import (
    ProductsTabPresenter,
)
from src.features.reports.presentation.controllers.ReportsTabPresenter import (
    ReportsTabPresenter,
)
from src.features.transactions.presentation.controllers.TransactionTabPresenter import (
    TransactionTabPresenter,
)


class AddTransactionMediator:
    def __init__(
        self,
        transaction_tab_presenter: TransactionTabPresenter,
        products_tab_presenter: ProductsTabPresenter,
        reports_tab_presenter: ReportsTabPresenter,
    ):
        self.transaction_tab_presenter = transaction_tab_presenter
        self.products_tab_presenter = products_tab_presenter
        self.reports_tab_presenter = reports_tab_presenter

        self.transaction_tab_presenter.set_on_transaction_created(
            self.products_tab_presenter.on_load_products_requested
        )
        self.transaction_tab_presenter.set_on_transaction_created(
            self.reports_tab_presenter.on_load_transactions_requested
        )
