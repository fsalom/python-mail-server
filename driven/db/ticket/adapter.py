from datetime import datetime

from asgiref.sync import sync_to_async
from django.db import models

from application.ports.driven.database.ticket.db_repository import TicketDBRepositoryPort
from domain.date_range import DateRange
from domain.product import Product
from domain.ticket import Ticket
from driven.db.ticket.mapper import TicketDBMapper
from driven.db.ticket.models import TicketDBO, TicketProductDBO


class TicketDBRepositoryAdapter(TicketDBRepositoryPort):
    def __init__(self, mapper: TicketDBMapper):
        self.mapper = mapper

    def save(self, ticket: Ticket):
        store_dbo = TicketDBMapper.map_store(ticket)
        user_dbo = TicketDBMapper.map_user(ticket)
        ticket_dbo = TicketDBMapper.map_ticket(ticket, store_dbo, user_dbo)
        products_dbo = TicketDBMapper.map_products_of_ticket(ticket_dbo, ticket.products, ticket.date)
        ticket_dbo.products.set(products_dbo)

    async def update_existing_tickets(self) -> None:
        def _update_existing_tickets(tickets) -> None:
            for ticket in tickets:
                if ticket.date_raw:
                    try:
                        parsed_datetime = datetime.strptime(ticket.date_raw, '%d/%m/%Y %H:%M')
                        ticket.date = parsed_datetime.date()
                        ticket.time = parsed_datetime.time()
                        ticket.save()
                    except ValueError:
                        print(f"Error: Formato de date_raw incorrecto en el ticket con id {ticket.id_ticket}")

        tickets = TicketDBO.objects.all()
        await sync_to_async(_update_existing_tickets)(tickets)

    async def get_tickets_for(self, user: str) -> [Ticket]:
        def _get_tickets(current_user) -> [Ticket]:
            ticket_dbo_list = TicketDBO.objects.filter(email__email=current_user)
            return TicketDBMapper.to_dbos(ticket_dbo_list)

        tickets = await sync_to_async(_get_tickets)(user)
        return tickets

    async def get_total_for(self, user: str, date_range: DateRange) -> float:
        def _get_total(current_user, _date_range) -> float:
            tickets = TicketDBO.objects.filter(
                email__email=current_user,
                date__gte=_date_range.start,
                date__lte=_date_range.end
            )
            return tickets.aggregate(total=models.Sum('total'))['total'] or 0.0

        total = await sync_to_async(_get_total)(user, date_range)
        return total

    async def get_number_of_tickets_for(self, user: str, date_range: DateRange) -> int:
        def _get_ticket_count(current_user, _date_range) -> int:
            return TicketDBO.objects.filter(
                email__email=current_user,
                date__gte=_date_range.start,
                date__lte=_date_range.end
            ).count()

        count = await sync_to_async(_get_ticket_count)(user, date_range)
        return count

    async def get_number_of_products_for(self, user: str, date_range: DateRange) -> int:
        def _get_product_count(current_user, _date_range) -> int:
            tickets = TicketDBO.objects.filter(
                email__email=current_user,
                date__gte=_date_range.start,
                date__lte=_date_range.end
            )
            return TicketProductDBO.objects.filter(ticket__in=tickets).aggregate(
                total_quantity=models.Sum('quantity')
            )['total_quantity'] or 0

        count = await sync_to_async(_get_product_count)(user, date_range)
        return count

    async def get_top_products_for(self, user: str, date_range: DateRange, number: int = 10) -> [Product]:
        def _get_top_products(current_user, _date_range, number) -> [Product]:
            tickets = TicketDBO.objects.filter(
                email__email=current_user,
                date__gte=_date_range.start,
                date__lte=_date_range.end
            )

            _top_products = TicketProductDBO.objects.filter(ticket__in=tickets).values(
                'product'
            ).annotate(
                total_quantity=models.Sum('quantity')
            ).order_by('-total_quantity').distinct()[:number]

            return [
                TicketDBMapper.ticket_product_dbo_to_domain(TicketProductDBO.objects.get(id=product['product']))
                for product in _top_products
            ]

        top_products = await sync_to_async(_get_top_products)(user, date_range, number)
        return top_products
