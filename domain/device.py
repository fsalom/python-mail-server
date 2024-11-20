from typing import Optional, Literal
from pydantic import Field, BaseModel


class Device(BaseModel):
    user_id: Optional[int] = Field(default=None)
    device_id: str
    platform: Literal['ios', 'android']
