from src.features.stock_info.domain.entities.StockItem import StockItem
from src.features.transactions.application.dtos.TransactionDisplayDTO import (
    TransactionDisplayDTO,
)
from src.features.transactions.domain.entities.Transaction import Transaction
from src.shared.application.dtos.ProcessDTO import ProcessDTO
from src.shared.application.Interfaces.IStockItemsRepository import (
    IStockItemsRepository,
)
from src.shared.application.Interfaces.ITransactionsRepository import (
    ITransactionsRepository,
)
from src.shared.application.usecases.Decorators.BaseUseCaseDecorator import usecase_func


class AddTransactionUseCase:
    def __init__(
        self,
        transactions_db: ITransactionsRepository,
        stock_items_db: IStockItemsRepository,
    ):
        self.stock_items_db = stock_items_db
        self.transactions_db = transactions_db

    @usecase_func
    def execute(self, dto: TransactionDisplayDTO) -> ProcessDTO:
        if not dto.items:
            return ProcessDTO(
                status=False,
                message="В транзакции не указаны продукты!",
                error="Products are not selected",
            )

        if not dto.branch_id:
            return ProcessDTO(
                status=False,
                message="Не указан филиал!",
                error="Branch is not selected",
            )

        if not dto.warehouse_id:
            return ProcessDTO(
                status=False,
                message="Не указан склад!",
                error="Warehouse is not selected",
            )

        if not dto.is_arrival:
            for item in dto.items:
                stock_item = self.stock_items_db.get_item_in_stock(
                    dto.branch_id, dto.warehouse_id, item.product_id
                )

                if stock_item.quantity < item.quantity:
                    return ProcessDTO(
                        status=False,
                        message=f"Недостаточно продуктов на складе: {item.product_name}",
                        error=f"Product {item.product_name} in warehouse is less than required",
                    )
                elif stock_item.quantity == item.quantity:
                    self.stock_items_db.delete_item_in_stock(
                        dto.branch_id, dto.warehouse_id, item.product_id
                    )
                else:
                    stock_item.quantity -= item.quantity

                    self.stock_items_db.change_item_in_stock(stock_item)
        else:
            for item in dto.items:
                stock_item = self.stock_items_db.get_item_in_stock(
                    dto.branch_id, dto.warehouse_id, item.product_id
                )

                if not stock_item:
                    stock_item = StockItem(
                        branch_id=dto.branch_id,
                        stock_id=dto.warehouse_id,
                        product_id=item.product_id,
                        quantity=item.quantity,
                    )

                    self.stock_items_db.add_item_in_stock(stock_item)
                else:
                    stock_item.quantity += item.quantity

                    self.stock_items_db.change_item_in_stock(stock_item)

        transaction = Transaction.model_validate(dto.model_dump())

        self.transactions_db.log_transaction(transaction)

        return ProcessDTO(status=True, message="Транзакция создана успешно!")
