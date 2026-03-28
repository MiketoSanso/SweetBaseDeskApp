from pydantic import BaseModel


class StockItem(BaseModel):
    local_id: int | None = None
    server_id: int | None = None
    branch_id: int
    stock_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True
