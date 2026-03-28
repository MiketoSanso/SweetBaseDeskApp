from pydantic import BaseModel


class StockItemDisplayDTO(BaseModel):
    branch_name: str
    warehouse_name: str
    quantity: int
