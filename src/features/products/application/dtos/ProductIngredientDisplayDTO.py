from pydantic import BaseModel


class ProductIngredientDisplayDTO(BaseModel):
    id: int
    name: str
    quantity: int
    unit: str
    cost: float
