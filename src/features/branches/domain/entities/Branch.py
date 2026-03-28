from typing import List

from pydantic import BaseModel


class Branch(BaseModel):
    local_id: int | None = None
    server_id: int | None = None
    name: str
    warehouses: List[int]

    class Config:
        from_attributes = True
