from pydantic import BaseModel, ConfigDict


class Ingredient(BaseModel):
    local_id: int | None = None
    server_id: int | None = None
    name: str
    unit_cost: float
    unit: str
    description: str | None = None
    count_usages: int = 0

    model_config = ConfigDict(from_attributes=True)
