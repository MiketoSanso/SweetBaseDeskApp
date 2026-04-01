from sqlalchemy import func
from sqlalchemy.engine import row

from src.features.stock_info.domain.entities.StockItem import StockItem
from src.features.stock_info.infrastructure.models.StockItemORM import StockItemORM
from src.shared.application.Interfaces.IStockItemsRepository import (
    IStockItemsRepository,
)
from src.shared.infrastructure.Database import Database
from src.shared.infrastructure.repositories.Decorators.RepositoryDecorator import (
    repo_func,
)


class StockItemsRepository(IStockItemsRepository):
    def __init__(self, db: Database):
        super().__init__(db)

    @repo_func
    def get_count_product_in_stocks(self, id: int, session=None) -> int:
        items = session.query(StockItemORM).filter(StockItemORM.product_id == id).all()
        count = 0

        for item in items:
            count += item.quantity

        return count

    @repo_func
    def get_all_count_stocks(self, id_stock_items: tuple[int, ...], session=None) -> dict[int, int]:
        result = session.query(
            StockItemORM.local_id,
            func.sum(StockItemORM.quantity).label('total_quantity')
        ).filter(StockItemORM.product_id.in_(id_stock_items)
                 ).group_by(StockItemORM.product_id
                            ).all()


        stock_counts = {row.local_id: row.total_quantity for row in result}

        return stock_counts

    @repo_func
    def get_item_in_stock(
        self, branch_id: int, stock_id: int, product_id: int, session=None
    ) -> StockItem | None:
        item_orm = (
            session.query(StockItemORM)
            .filter(
                StockItemORM.branch_id == branch_id,
                StockItemORM.stock_id == stock_id,
                StockItemORM.product_id == product_id,
            )
            .first()
        )

        if not item_orm:
            return None

        item = StockItem.model_validate(item_orm)

        return item

    @repo_func
    def get_items_in_stock(
        self, branch_id: int, stock_id: int, session=None
    ) -> list[StockItem] | None:
        items_orm = (
            session.query(StockItemORM)
            .filter(
                StockItemORM.branch_id == branch_id, StockItemORM.stock_id == stock_id
            )
            .all()
        )

        items = []

        for item in items_orm:
            new_item = StockItem.model_validate(item)
            items.append(new_item)

        if not items:
            return None

        return items

    @repo_func
    def get_stock_items(self, branch_id: int, session=None) -> tuple[StockItem] | None:
        items_orm = (
            session.query(StockItemORM)
            .filter(StockItemORM.branch_id == branch_id)
            .all()
        )

        if not items_orm:
            return None

        items = []
        for item in items_orm:
            items.append(StockItem.model_validate(item))

        return items

    @repo_func
    def add_item_in_stock(self, stock_item: StockItem, session=None):
        orm = StockItemORM(**stock_item.model_dump())
        session.add(orm)

    @repo_func
    def change_item_in_stock(self, stock_item: StockItem, session=None):
        orm = (
            session.query(StockItemORM)
            .filter(
                StockItemORM.branch_id == stock_item.branch_id,
                StockItemORM.stock_id == stock_item.stock_id,
                StockItemORM.product_id == stock_item.product_id,
            )
            .first()
        )

        if orm:
            orm.quantity = stock_item.quantity

    @repo_func
    def delete_item_in_stock(
        self, branch_id: int, stock_id: int, product_id: int, session=None
    ):
        item_orm = (
            session.query(StockItemORM)
            .filter(
                StockItemORM.branch_id == branch_id,
                StockItemORM.stock_id == stock_id,
                StockItemORM.product_id == product_id,
            )
            .first()
        )

        if item_orm:
            session.delete(item_orm)
