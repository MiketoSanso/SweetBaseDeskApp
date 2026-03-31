from typing import Callable, List

from src.features.branches.application.interfaces.IBranchesTab import IBranchesTab
from src.features.branches.application.usecases.AddBranchUseCase import AddBranchUseCase
from src.features.branches.application.usecases.GetBranchesUseCase import (
    GetBranchesUseCase,
)
from src.features.branches.presentation.controllers.AddBranchDialogPresenter import (
    AddBranchDialogPresenter,
)
from src.features.branches.presentation.PQ.dialogs.AddBranchDialog import (
    AddBranchDialog,
)
from src.shared.application.Interfaces.IMessageService import IMessageService


class BranchTabPresenter:
    def __init__(
        self,
        view: IBranchesTab,
        message_service: IMessageService,
        add_branch_usecase: AddBranchUseCase,
        get_branches_usecase: GetBranchesUseCase,
    ):
        self.view = view
        self.message_service = message_service
        self.add_branch_usecase = add_branch_usecase
        self.get_branches_usecase = get_branches_usecase

        self.callbacks: List[Callable[[], None]] = []

        self.view.set_on_add_branch_requested(self.on_add_branch_requested)
        self.view.set_on_load_branches_requested(self.on_load_branches_requested)
        self._display_branches()

    def on_add_branch_requested(self):
        dialog = AddBranchDialog()

        self._dialog_presenter = AddBranchDialogPresenter(
            view=dialog,
            message_service=self.message_service,
            add_branch_usecase=self.add_branch_usecase,
        )

        self._dialog_presenter.set_on_success_callback(self._display_branches)
        self._dialog_presenter.set_on_success_callback(self._on_branches_updated)

        dialog.exec()

    def set_on_branches_updated(self, callback: Callable[[], None]):
        self.callbacks.append(callback)

    def on_load_branches_requested(self):
        self._display_branches()

    def _display_branches(self):
        result = self.get_branches_usecase.execute()
        self.view.display_branches(result.data, result.status)

    def _on_branches_updated(self):
        for callback in self.callbacks:
            callback()
