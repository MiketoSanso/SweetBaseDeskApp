from sqlalchemy import JSON, Column, Integer, String

from src.shared.infrastructure.Base import Base


class BranchORM(Base):
    __tablename__ = "branches"

    local_id = Column(Integer, primary_key=True)
    server_id = Column(Integer)
    name = Column(String, nullable=False)
    warehouses = Column(JSON, default=list)

    __mapper_args__ = {"primary_key": [local_id]}
