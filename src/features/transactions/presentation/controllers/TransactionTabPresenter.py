from datetime import datetime
from typing import Callable

from src.features.branches.application.usecases.GetBranchesUseCase import (
    GetBranchesUseCase,
)
from src.features.products.application.usecases.GetProductsUseCase import (
    GetProductsUseCase,
)
from src.features.transactions.application.dtos.TransactionDisplayDTO import (
    TransactionDisplayDTO,
)
from src.features.transactions.application.interfaces.ITransactionTab import (
    ITransactionTab,
)
from src.features.transactions.application.usecases.AddTransactionUseCase import (
    AddTransactionUseCase,
)
from src.features.transactions.application.usecases.GetWarehousesUseCase import (
    GetWarehousesUseCase,
)
from src.features.transactions.application.value_objects.TransactionItem import (
    TransactionItem,
)
from src.features.transactions.presentation.controllers.TransactionItemsDialogPresenter import (
    TransactionItemsDialogPresenter,
)
from src.features.transactions.presentation.PQ.dialogs.TransactionItemsDialog import (
    TransactionItemsDialog,
)
from src.shared.application.Interfaces.IMessageService import IMessageService


class TransactionTabPresenter:
    def __init__(
        self,
        view: ITransactionTab,
        message_service: IMessageService,
        add_transaction_usecase: AddTransactionUseCase,
        get_products_dto: GetProductsUseCase,
        get_branches_usecase: GetBranchesUseCase,
        get_warehouses_usecase: GetWarehousesUseCase,
    ):
        self.view = view
        self.message_service = message_service
        self.add_transaction_usecase = add_transaction_usecase
        self.get_products_dto = get_products_dto
        self.get_branches_usecase = get_branches_usecase
        self.get_warehouses_usecase = get_warehouses_usecase

        self.items: list[TransactionItem] = []
        self._create_callbacks: list[Callable[[], None]] = []

        self.view.set_on_add_items_requested(self.on_add_items_requested)
        self.view.set_on_process_transaction_requested(
            self.on_process_transaction_requested
        )
        self.view.set_on_change_branch_requested(self.set_warehouses)

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

    def on_add_items_requested(self):
        dialog = TransactionItemsDialog()

        presenter = TransactionItemsDialogPresenter(
            dialog, self.message_service, self.get_products_dto
        )

        presenter.set_on_items_confirmed(self.set_transaction_items)

        dialog.exec()

    def on_process_transaction_requested(self, data: dict):
        total_qty = sum(item.quantity for item in self.items)

        if not data["branch_id"] or not data["warehouse_id"]:
            self.message_service.show_error(
                "Ошибка", "Данные для сохранения не указаны!", self.view
            )
            return

        transaction = TransactionDisplayDTO(
            is_arrival=data["is_arrival"],
            branch_id=data["branch_id"],
            warehouse_id=data["warehouse_id"],
            items=self.items,
            total_amount=total_qty,
            timestamp=datetime.now(),
            user_note=data["note"],
        )

        result_dto = self.add_transaction_usecase.execute(transaction)

        if result_dto.status:
            self.message_service.show_success("Успех", result_dto.message, self.view)
            self.items.clear()
            self.view.update_display(self.items)

            for callback in self._create_callbacks:
                callback()
        else:
            self.message_service.show_success("Ошибка", result_dto.message, self.view)

    def set_on_transaction_created(self, callback: Callable[[], None]):
        self._create_callbacks.append(callback)

    def set_transaction_items(self, items: list[TransactionItem]):
        self.items.extend(items)
        self.view.update_display(self.items)
