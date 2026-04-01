 

from src.features.reports.application.dtos.TransactionFiltersDTO import (
    TransactionFiltersDTO,
)
from src.features.reports.application.dtos.TransactionsInfoDTO import (
    TransactionsInfoDTO,
)
from src.features.transactions.domain.entities.Transaction import Transaction
from src.features.transactions.infrastructure.models.TransactionORM import (
    TransactionORM,
)
from src.shared.application.Interfaces.ITransactionsRepository import (
    ITransactionsRepository,
)
from src.shared.infrastructure.Database import Database
from src.shared.infrastructure.repositories.Decorators.RepositoryDecorator import (
    repo_func,
)
from src.shared.infrastructure.repositories.ProductsRepository import ProductsRepository


class TransactionsRepository(ITransactionsRepository):
    def __init__(self, db: Database, data_products: ProductsRepository):
        super().__init__(db, data_products)

    @repo_func
    def log_transaction(self, transaction: Transaction, session=None):
        transaction_orm = TransactionORM(**transaction.model_dump())

        session.add(transaction_orm)

    @repo_func
    def get_transactions_info(self, session=None) -> TransactionsInfoDTO:
        in_count = (
            session.query(TransactionORM)
            .filter(TransactionORM.is_arrival is True)
            .count()
        )
        out_count = (
            session.query(TransactionORM)
            .filter(TransactionORM.is_arrival is False)
            .count()
        )

        last = session.query(TransactionORM).order_by(TransactionORM.timestamp).first()

        if last:
            last_date = last.timestamp
        else:
            last_date = None

        transaction_info = TransactionsInfoDTO(
            total_transactions=in_count + out_count,
            in_count=in_count,
            out_count=out_count,
            last_transaction_date=last_date,
        )

        return transaction_info

    @repo_func
    def get_transactions(
        self, filters: TransactionFiltersDTO = None, session=None
    ) -> list[Transaction]:
        query = session.query(TransactionORM)

        if filters:
            if filters.is_arrival:
                query = query.filter(TransactionORM.is_arrival == filters.is_arrival)
            if filters.branch_id != 0:
                query = query.filter(TransactionORM.branch_id == filters.branch_id)
            if filters.warehouse_id != 0:
                query = query.filter(
                    TransactionORM.warehouse_id == filters.warehouse_id
                )
            if filters.date_from:
                query = query.filter(TransactionORM.timestamp >= filters.date_from)
            if filters.date_to:
                query = query.filter(TransactionORM.timestamp <= filters.date_to)

        transactions = [Transaction.model_validate(item) for item in query]

        return transactions
