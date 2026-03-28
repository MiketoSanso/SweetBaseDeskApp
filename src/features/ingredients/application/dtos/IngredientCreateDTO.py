from pydantic import BaseModel


class IngredientCreateDTO(BaseModel):
    name: str
    unit: str
    unit_cost: float
    description: str | None = None
