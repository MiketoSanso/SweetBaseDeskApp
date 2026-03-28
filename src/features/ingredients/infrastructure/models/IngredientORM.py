from sqlalchemy import Column, Float, Integer, String

from src.shared.infrastructure.Base import Base


class IngredientORM(Base):
    __tablename__ = "ingredients"

    local_id = Column(Integer, primary_key=True)
    server_id = Column(Integer)
    name = Column(String, nullable=False)
    unit_cost = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    description = Column(String, nullable=False)
    count_usages = Column(Integer)

    __mapper_args__ = {"primary_key": [local_id]}
