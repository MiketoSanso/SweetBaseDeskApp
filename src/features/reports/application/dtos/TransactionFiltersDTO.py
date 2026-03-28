from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TransactionFiltersDTO(BaseModel):
    is_arrival: bool
    branch_id: int
    warehouse_id: int
    date_from: Optional[datetime]
    date_to: Optional[datetime]
