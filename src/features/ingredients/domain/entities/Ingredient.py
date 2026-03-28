from pydantic import BaseModel


class Ingredient(BaseModel):
    local_id: int | None = None
    server_id: int | None = None
    name: str
    unit_cost: float
    unit: str
    description: str | None = None
    count_usages: int = 0

    class Config:
        from_attributes = True
