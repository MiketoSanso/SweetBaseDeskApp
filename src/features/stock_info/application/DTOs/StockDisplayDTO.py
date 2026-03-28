from pydantic import BaseModel


class StockDisplayDTO(BaseModel):
    product_name: str
    quantity: int
    cost: float
