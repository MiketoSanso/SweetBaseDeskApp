from pydantic import BaseModel


class ObjectDisplayDTO(BaseModel):
    object_id: int
    object_name: str
