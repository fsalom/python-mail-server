from dataclasses import Field
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: Optional[int] = None
    email: str
