from pydantic import BaseModel, ConfigDict
from typing import Optional


class CoreSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: Optional[int] = None
