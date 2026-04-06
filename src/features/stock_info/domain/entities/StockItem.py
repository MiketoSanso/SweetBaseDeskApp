from pydantic import BaseModel, ConfigDict


class StockItem(BaseModel):
    local_id: int | None = None
    server_id: int | None = None
    branch_id: int
    stock_id: int
    product_id: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)
