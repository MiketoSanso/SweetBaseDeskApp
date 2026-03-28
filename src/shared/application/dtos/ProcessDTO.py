from typing import Any, Optional

from pydantic import BaseModel


class ProcessDTO(BaseModel):
    status: bool
    message: str = ""
    data: Optional[Any] = None
    error: Optional[str] = None
