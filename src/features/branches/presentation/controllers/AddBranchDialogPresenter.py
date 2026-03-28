from typing import Callable

from src.features.branches.application.dtos.BranchCreateDTO import BranchCreateDTO
from src.features.branches.application.interfaces.IAddBranchDialog import (
    IAddBranchDialog,
)
from src.features.branches.application.usecases.AddBranchUseCase import AddBranchUseCase
from src.shared.application.Interfaces.IMessageService import IMessageService


class AddBranchDialogPresenter:
    def __init__(
        self,
        view: IAddBranchDialog,
        message_service: IMessageService,
        add_branch_usecase: AddBranchUseCase,
    ):
        self.view = view
        self.message_service = message_service
        self.add_branch_usecase = add_branch_usecase

        self._success_callbacks = []

        self.view.set_on_branch_data_entered(self._on_branch_data_entered)

    def _on_branch_data_entered(self, data: dict):
        warehouses = [i for i in range(1, data["warehouses_count"] + 1)]

        branch_dto = BranchCreateDTO(name=data["name"], warehouses=warehouses)

        process_dto = self.add_branch_usecase.execute(branch_dto)
        if process_dto.status:
            self.message_service.show_success("Успех", process_dto.message, self.view)

            for callback in self._success_callbacks:
                callback()

            self.view.close_dialog()
        else:
            self.message_service.show_error("Ошибка", process_dto.message, self.view)

    def set_on_success_callback(self, callback: Callable[[], None]):
        self._success_callbacks.append(callback)
