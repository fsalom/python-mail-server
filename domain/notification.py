from typing import Any, Dict, Optional
from pydantic import Field, BaseModel
from domain.user import User


class Notification(BaseModel):
    id: int
    title: str
    content: str
    data: Optional[Dict[str, Any]] = Field(default=None)
    created_by: User
