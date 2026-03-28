from sqlalchemy import Column, Integer, UniqueConstraint

from src.shared.infrastructure.Base import Base


class StockItemORM(Base):
    __tablename__ = "stock_items"

    local_id = Column(Integer, primary_key=True)
    server_id = Column(Integer)
    branch_id = Column(Integer, nullable=False)  # ,index=True)
    stock_id = Column(Integer, nullable=False)  # ,index=True)
    product_id = Column(Integer, nullable=False)  # ,index=True)
    quantity = Column(Integer, default=0, nullable=False)

    __mapper_args__ = {"primary_key": [local_id]}

    __table_args__ = (
        UniqueConstraint(
            "branch_id", "stock_id", "product_id", name="unique_stock_item"
        ),
        # Index('ix_stock_lookup', 'branch_id', 'stock_id', 'product_id'),
    )
