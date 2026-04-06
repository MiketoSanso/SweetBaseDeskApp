from pydantic import BaseModel, ConfigDict


class Branch(BaseModel):
    local_id: int | None = None
    server_id: int | None = None
    name: str
    warehouses: list[int]

    model_config = ConfigDict(from_attributes=True)
