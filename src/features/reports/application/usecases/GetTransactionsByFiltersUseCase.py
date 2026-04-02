from src.features.reports.application.dtos.ReportTransactionDTO import (
    ReportTransactionDTO,
)
from src.features.reports.application.dtos.TransactionFiltersDTO import (
    TransactionFiltersDTO,
)
from src.shared.application.dtos.ProcessDTO import ProcessDTO
from src.shared.application.usecases.Decorators.BaseUseCaseDecorator import usecase_func
from src.shared.infrastructure.repositories.BranchesRepository import BranchesRepository
from src.shared.infrastructure.repositories.TransactionsRepository import (
    TransactionsRepository,
)


class GetTransactionsByFiltersUseCase:
    def __init__(
        self,
        transactions_repo: TransactionsRepository,
        branches_repo: BranchesRepository,
    ):
        self.transactions_repo = transactions_repo
        self.branches_repo = branches_repo

    @usecase_func
    def execute(self, transaction_filters: TransactionFiltersDTO) -> ProcessDTO:
        transactions = self.transactions_repo.get_transactions(transaction_filters)

        dto_transactions = []

        for transaction in transactions:
            branch = self.branches_repo.get_branch_by_id(transaction.branch_id)

            type = "Приход" if transaction.is_arrival else "Уход"

            text_item = ""

            for item in transaction.items:
                text_item += f"{item.product_name}, "

            dto_transactions.append(
                ReportTransactionDTO(
                    type=type,
                    branch_name=branch.name,
                    warehouse_name=f"Склад_{transaction.warehouse_id}",
                    items_text=text_item,
                    total_amount=transaction.total_amount,
                    timestamp=transaction.timestamp,
                    user_note=transaction.user_note,
                )
            )

        return ProcessDTO(
            status=True,
            message="Транзакции успешно отсортированы!",
            data=dto_transactions,
        )
