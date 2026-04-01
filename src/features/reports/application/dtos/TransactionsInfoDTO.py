from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TransactionsInfoDTO(BaseModel):
    total_transactions: int
    in_count: int
    out_count: int
    last_transaction_date: Optional[datetime]
