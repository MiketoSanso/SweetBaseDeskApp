from abc import ABC, abstractmethod
from typing import Tuple

from src.features.stock_info.domain.entities.StockItem import StockItem
from src.shared.infrastructure.Database import Database


class IStockItemsRepository(ABC):
    def __init__(self, db: Database):
        self.db = db

    @abstractmethod
    def get_count_product_in_stocks(self, id: int) -> int:
        pass

    @abstractmethod
    def get_all_count_stocks(self, id_stock_items: tuple[int], session=None) -> tuple[int]:
        pass

    @abstractmethod
    def get_item_in_stock(
        self, branch_id: int, stock_id: int, product_id: int
    ) -> StockItem | None:
        pass

    @abstractmethod
    def get_stock_items(self, branch_id: int) -> Tuple[StockItem] | None:
        pass

    @abstractmethod
    def add_item_in_stock(self, stock_item: StockItem):
        pass

    @abstractmethod
    def change_item_in_stock(self, stock_item: StockItem):
        pass

    @abstractmethod
    def delete_item_in_stock(self, branch_id: int, stock_id: int, product_id: int):
        pass
