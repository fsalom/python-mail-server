from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from domain.ticket import Ticket


class TicketsMonth(BaseModel):
    month: str
    num_tickets: int
    total: float
    total_difference: Optional[float] = None
    tickets: List[Ticket]

    model_config = ConfigDict(arbitrary_types_allowed=True)
