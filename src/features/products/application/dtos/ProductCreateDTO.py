from typing import List

from pydantic import BaseModel

from src.features.products.domain.value_objects.ProductIngredientVO import (
    ProductIngredientVO,
)


class ProductCreateDTO(BaseModel):
    name: str
    ingredients: List[ProductIngredientVO]
