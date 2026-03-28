from datetime import datetime

from pydantic import BaseModel


class ReportTransactionDTO(BaseModel):
    type: str
    branch_name: str
    warehouse_name: str
    items_text: str
    total_amount: float
    timestamp: datetime
    user_note: str
