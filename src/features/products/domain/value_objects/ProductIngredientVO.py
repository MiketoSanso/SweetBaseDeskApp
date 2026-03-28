from pydantic import BaseModel, ConfigDict


class ProductIngredientVO(BaseModel):
    ingredient_id: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)
