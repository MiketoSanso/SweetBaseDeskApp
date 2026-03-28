from abc import ABC, abstractmethod
from typing import List

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
    def get_transactions(self, filters: dict = None) -> List[Transaction] | None:
        pass
