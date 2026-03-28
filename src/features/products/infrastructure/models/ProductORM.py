from sqlalchemy import JSON, Column, Integer, String

from src.shared.infrastructure.Base import Base


class ProductORM(Base):
    __tablename__ = "products"

    local_id = Column(Integer, primary_key=True)
    server_id = Column(Integer)
    name = Column(String, nullable=False)
    image_path = Column(String, nullable=True)
    ingredients = Column(JSON, default=list)

    __mapper_args__ = {"primary_key": [local_id]}
