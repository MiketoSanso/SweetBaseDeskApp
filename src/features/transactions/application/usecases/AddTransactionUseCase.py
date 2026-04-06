from src.features.stock_info.domain.entities.StockItem import StockItem
from src.features.transactions.application.dtos.TransactionDisplayDTO import (
    TransactionDisplayDTO,
)
from src.features.transactions.domain.entities.Transaction import Transaction
from src.shared.application.dtos.ProcessDTO import ProcessDTO
from src.shared.application.Interfaces.IBranchesRepository import IBranchesRepository
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
        transactions_repo: ITransactionsRepository,
        stock_items_repo: IStockItemsRepository,
        branches_repo: IBranchesRepository,
    ):
        self.stock_items_repo = stock_items_repo
        self.transactions_repo = transactions_repo
        self.branches_repo = branches_repo

    @usecase_func
    def execute(self, dto: TransactionDisplayDTO) -> ProcessDTO:
        if not dto.items:
            return ProcessDTO(
                status=False,
                message="В транзакции не указаны продукты!",
                error="Products are not selected",
            )

        if dto.branch_id < 0:
            return ProcessDTO(
                status=False,
                message="Неверно указан id филиала!",
                error="Branch id is incorrect",
            )

        if dto.warehouse_id < 0:
            return ProcessDTO(
                status=False,
                message="Неверно указан id склада!",
                error="Warehouse id is incorrect",
            )

        if dto.total_amount < 0 or dto.total_amount is not sum(
            item.quantity for item in dto.items
        ):
            return ProcessDTO(
                status=False,
                message="Неверно указано общее количество объектов!",
                error="Total amount is incorrect",
            )

        if not dto.is_arrival:
            for item in dto.items:
                stock_item = self.stock_items_repo.get_item_in_stock(
                    dto.branch_id, dto.warehouse_id, item.product_id
                )

                if not stock_item:
                    return ProcessDTO(
                        status=False,
                        message="Переданы некорректные ID объекта!",
                        error="Branch/Warehouse/Product ID is incorrect!",
                    )

                if stock_item.quantity < item.quantity:
                    return ProcessDTO(
                        status=False,
                        message=f"Недостаточно продуктов на складе: "
                        f"{item.product_name}",
                        error=f"Product {item.product_name} "
                        f"in warehouse is less than required",
                    )
                elif stock_item.quantity == item.quantity:
                    self.stock_items_repo.delete_item_in_stock(
                        dto.branch_id, dto.warehouse_id, item.product_id
                    )
                else:
                    stock_item.quantity -= item.quantity

                    self.stock_items_repo.change_item_in_stock(stock_item)
        else:
            for item in dto.items:
                warehouse = None
                branch = self.branches_repo.get_branch_by_id(dto.branch_id)
                if branch:
                    warehouse = branch.warehouses[dto.warehouse_id]

                if not warehouse or not branch:
                    return ProcessDTO(
                        status=False,
                        message="Переданы некорректные ID объекта!",
                        error="Branch/Warehouse/Product ID is incorrect!",
                    )

                stock_item = self.stock_items_repo.get_item_in_stock(
                    dto.branch_id, dto.warehouse_id, item.product_id
                )

                if not stock_item:
                    stock_item = StockItem(
                        branch_id=dto.branch_id,
                        stock_id=dto.warehouse_id,
                        product_id=item.product_id,
                        quantity=item.quantity,
                    )

                    self.stock_items_repo.add_item_in_stock(stock_item)
                else:
                    stock_item.quantity += item.quantity

                    self.stock_items_repo.change_item_in_stock(stock_item)

        transaction = Transaction.model_validate(dto.model_dump())

        self.transactions_repo.log_transaction(transaction)

        return ProcessDTO(status=True, message="Транзакция создана успешно!")
