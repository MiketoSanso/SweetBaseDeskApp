from src.shared.application.dtos.ProcessDTO import ProcessDTO
from src.shared.application.usecases.Decorators.BaseUseCaseDecorator import usecase_func
from src.shared.infrastructure.repositories.TransactionsRepository import (
    TransactionsRepository,
)


class GetTransactionsInfoUseCase:
    def __init__(self, transactions_repo: TransactionsRepository):
        self.transactions_repo = transactions_repo

    @usecase_func
    def execute(self) -> ProcessDTO:
        transactions_info = self.transactions_repo.get_transactions_info()

        return ProcessDTO(
            status=True,
            message="Данные о транзакциях загружены!",
            data=transactions_info,
        )
