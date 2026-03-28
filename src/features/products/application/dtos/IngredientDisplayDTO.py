from pydantic import BaseModel


class IngredientDisplayDTO(BaseModel):
    name: str
    quantity: int
    unit: str
    unit_cost: int
