from pydantic import BaseModel, ConfigDict


class TransactionItem(BaseModel):
    product_id: int
    quantity: int
    product_name: str = ""

    model_config = ConfigDict(from_attributes=True)
