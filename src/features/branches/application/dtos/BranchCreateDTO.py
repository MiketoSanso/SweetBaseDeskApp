from typing import List

from pydantic import BaseModel


class BranchCreateDTO(BaseModel):
    name: str
    warehouses: List[int]
