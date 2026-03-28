from src.features.branches.presentation.controllers.BranchTabPresenter import (
    BranchTabPresenter,
)
from src.features.transactions.presentation.controllers.TransactionTabPresenter import (
    TransactionTabPresenter,
)


class CreateBranchMediator:
    def __init__(
        self,
        branch_tab_presenter: BranchTabPresenter,
        transaction_tab_presenter: TransactionTabPresenter,
    ):
        self.branch_tab_presenter = branch_tab_presenter
        self.transaction_tab_presenter = transaction_tab_presenter

        self.branch_tab_presenter.set_on_branches_updated(
            self.transaction_tab_presenter.set_branches
        )
