from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from domain.date_range import DateRange
from domain.product import Product
from domain.ticket import Ticket
from domain.ticket_month import TicketsMonth


class TicketDBRepositoryPort(ABC):
    @abstractmethod
    def save(self, ticket: Ticket):
        pass

    @abstractmethod
    async def get_tickets_for(self, user: str) -> [Ticket]:
        pass

    @abstractmethod
    async def update_existing_tickets(self) -> None:
        pass

    @abstractmethod
    async def get_total_for(self, user: str, date_range: DateRange) -> float:
        pass

    @abstractmethod
    async def get_number_of_tickets_for(self, user: str, date_range: DateRange) -> int:
        pass

    @abstractmethod
    async def get_number_of_products_for(self, user: str, date_range: DateRange) -> int:
        pass

    @abstractmethod
    async def get_top_products_for(self, user: str, date_range: DateRange, number: int = 10) -> [Product]:
        pass

    @abstractmethod
    async def get_tickets_grouped_by_month(self, user: str, date_range: DateRange) -> List[TicketsMonth]:
        pass
