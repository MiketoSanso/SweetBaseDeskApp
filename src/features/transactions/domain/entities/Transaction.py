from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict

from src.features.transactions.application.value_objects.TransactionItem import (
    TransactionItem,
)


class Transaction(BaseModel):
    local_id: int | None = None
    server_id: int | None = None
    is_arrival: bool
    branch_id: int
    warehouse_id: int
    items: List[TransactionItem]
    total_amount: float
    timestamp: datetime
    user_note: str

    model_config = ConfigDict(extra="ignore", from_attributes=True)
