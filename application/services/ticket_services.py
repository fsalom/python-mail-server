from asgiref.sync import sync_to_async

from application.ports.driven.database.ticket.db_repository import TicketDBRepositoryPort
from application.ports.driving.tickets_service_port import TicketServicePort
from domain.date_range import DateRange
from domain.product import Product
from domain.ticket import Ticket


class TicketServices(TicketServicePort):
    def __init__(self,
                 db_repository: TicketDBRepositoryPort):
        self.db_repository = db_repository

    async def get_ticket_for_user(self, user: str) -> [Ticket]:
        return await self.db_repository.get_tickets_for(user)

    async def get_number_of_products_for(self, user: str, date_range: DateRange) -> int:
        return await self.db_repository.get_number_of_products_for(user, date_range)

    async def get_number_of_tickets_for(self, user: str, date_range: DateRange) -> int:
        return await self.db_repository.get_number_of_tickets_for(user, date_range)

    async def get_total_for(self, user: str, date_range: DateRange) -> float:
        return await self.db_repository.get_total_for(user, date_range)

    async def get_top_products_for(self, user: str, date_range: DateRange, number: int = 10) -> [Product]:
        return await self.db_repository.get_top_products_for(user, date_range, number)

    async def update_existing_tickets(self):
        await self.db_repository.update_existing_tickets()
