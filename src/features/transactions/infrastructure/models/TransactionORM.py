from sqlalchemy import JSON, Boolean, Column, Float, Integer, String, DateTime

from src.shared.infrastructure.Base import Base


class TransactionORM(Base):
    __tablename__ = "transactions"

    local_id = Column(Integer, primary_key=True)
    server_id = Column(Integer)
    is_arrival = Column(Boolean, nullable=False)
    branch_id = Column(Integer, nullable=False)
    warehouse_id = Column(Integer, nullable=False)
    items = Column(JSON, default=list)
    total_amount = Column(Float)
    timestamp = Column(DateTime, nullable=False)
    user_note = Column(String, nullable=False)

    __mapper_args__ = {"primary_key": [local_id]}
