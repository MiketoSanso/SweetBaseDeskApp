from pydantic import BaseModel


class ProductDisplayDTO(BaseModel):
    id: int
    name: str
    stock_count: int
