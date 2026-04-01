from datetime import datetime
 

from pydantic import BaseModel, ConfigDict

from src.features.transactions.application.value_objects.TransactionItem import (
    TransactionItem,
)


class TransactionDisplayDTO(BaseModel):
    is_arrival: bool
    branch_id: int
    warehouse_id: int
    items: list[TransactionItem]
    total_amount: float
    timestamp: datetime
    user_note: str

    model_config = ConfigDict(extra="ignore")
