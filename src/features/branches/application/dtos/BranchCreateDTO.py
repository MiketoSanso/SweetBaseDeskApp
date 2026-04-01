 

from pydantic import BaseModel


class BranchCreateDTO(BaseModel):
    name: str
    warehouses: list[int]
