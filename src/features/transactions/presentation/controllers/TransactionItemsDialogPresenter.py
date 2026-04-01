from typing import Callable  

from src.features.products.application.usecases.GetProductsUseCase import (
    GetProductsUseCase,
)
from src.features.transactions.application.interfaces.ITransactionItemsDialog import (
    ITransactionItemsDialog,
)
from src.features.transactions.application.value_objects.TransactionItem import (
    TransactionItem,
)
from src.shared.application.dtos.ObjectDisplayDTO import ObjectDisplayDTO
from src.shared.application.Interfaces.IMessageService import IMessageService


class TransactionItemsDialogPresenter:
    def __init__(
        self,
        view: ITransactionItemsDialog,
        message_service: IMessageService,
        get_products_usecase: GetProductsUseCase,
    ):
        self.view = view
        self.message_service = message_service
        self.get_products_usecase = get_products_usecase

        self.items: list[TransactionItem] = []
        self.callbacks = []

        self.view.set_on_items_confirmed(self.on_items_confirmed)
        self.view.set_on_add_item_requested(self.on_add_item_requested)
        self.view.set_on_remove_item_requested(self.set_on_remove_item_requested)

        self.set_products()

    def set_products(self):
        result = self.get_products_usecase.execute()

        if not result.status:
            self.message_service.show_error("Ошибка", result.message, self.view)
            return

        view_products = []

        for product in result.data:
            product_dto = ObjectDisplayDTO(
                object_id=product.local_id, object_name=product.name
            )

            view_products.append(product_dto)

        self.view.set_products(view_products)

    def set_on_items_confirmed(self, callback: Callable[[list[TransactionItem]], None]):
        self.callbacks.append(callback)

    def on_items_confirmed(self):
        if not self.items:
            self.message_service.show_error(
                "Ошибка", "Добавьте хотя бы один товар!", self.view
            )
            return

        for callback in self.callbacks:
            callback(self.items)

        self.view.close_dialog()

    def on_add_item_requested(self, data: dict):
        for i, existing in enumerate(self.items):
            if existing.product_id == data["product_id"]:
                self.items[i].quantity += data["quantity"]
                self.view.update_table(self.items)
                return

        transaction_item = TransactionItem(
            product_id=data["product_id"],
            quantity=data["quantity"],
            product_name=data["name"],
        )

        self.items.append(transaction_item)
        self.view.update_table(self.items)

    def set_on_remove_item_requested(self, index: int):
        if 0 <= index < len(self.items):
            self.items.pop(index)
            self.view.update_table(self.items)
