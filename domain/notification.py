from typing import Any, Dict, Optional, List
from pydantic import Field, BaseModel
from domain.user import User


class Notification(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    data: Optional[Dict[str, Any]] = Field(default=None)
    created_by: User
    sent_to_device_ids: Optional[List[str]] = None
    invalid_device_ids: Optional[List[str]] = None
