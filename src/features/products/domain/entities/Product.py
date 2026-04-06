from pydantic import BaseModel, ConfigDict

from src.features.products.domain.value_objects.ProductIngredientVO import (
    ProductIngredientVO,
)


class Product(BaseModel):
    local_id: int | None = None
    server_id: int | None = None
    name: str
    image_path: str | None = None
    ingredients: list[ProductIngredientVO]

    model_config = ConfigDict(from_attributes=True)
