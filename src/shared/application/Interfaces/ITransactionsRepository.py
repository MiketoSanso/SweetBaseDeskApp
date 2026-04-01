from abc import ABC, abstractmethod
 

from src.features.transactions.domain.entities.Transaction import Transaction
from src.shared.application.Interfaces.IProductsRepository import IProductsRepository
from src.shared.infrastructure.Database import Database


class ITransactionsRepository(ABC):
    def __init__(self, db: Database, data_products: IProductsRepository):
        self.data_products = data_products
        self.db = db

    @abstractmethod
    def log_transaction(self, transaction: Transaction) -> bool:
        pass

    @abstractmethod
    def get_transactions(self, filters: dict = None) -> list[Transaction] | None:
        pass
