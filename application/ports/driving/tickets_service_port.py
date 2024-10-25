from abc import ABC, abstractmethod

from domain.date_range import DateRange
from domain.product import Product
from domain.ticket import Ticket


class TicketServicePort(ABC):
    @abstractmethod
    async def get_ticket_for_user(self, user: str) -> [Ticket]:
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
    async def update_existing_tickets(self):
        pass
