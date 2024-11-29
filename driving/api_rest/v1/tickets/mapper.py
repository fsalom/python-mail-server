from domain.date_range import DateRange
from domain.product import Product
from domain.ticket import Ticket
from domain.ticket_month import TicketsMonth
from driving.api_rest.v1.tickets.models import AllTicketsResponse, TicketResponse, ProductResponse, TicketsMonthResponse


class TicketDTOMapper:

    @staticmethod
    def to_dto(tickets: [Ticket]) -> AllTicketsResponse:
        return AllTicketsResponse(
            num_tickets=len(tickets),
            tickets=[
                TicketResponse(
                    id_ticket=ticket.id,
                    products=[ProductResponse(**vars(product)) for product in ticket.products],
                    total=ticket.total,
                    iva=ticket.iva,
                    date=ticket.date,
                    email=ticket.email,
                    location=ticket.location
                ) for ticket in tickets
            ])

    @staticmethod
    def products_to_dto(products: [Product]) -> [ProductResponse]:
        return [ProductResponse(name=product.name,
                                quantity=product.quantity,
                                price_per_unit=product.price_per_unit,
                                price=product.price,
                                weight=None) for product in products]

    @staticmethod
    def date_str_to_domain(start_date: str, end_date: str) -> DateRange:
        return DateRange(start_date=start_date, end_date=end_date)

    @staticmethod
    def tickets_to_dto(tickets: [Ticket]) -> [TicketResponse]:
        return [
                TicketResponse(
                    id_ticket=ticket.id,
                    products=[ProductResponse(**vars(product)) for product in ticket.products],
                    total=ticket.total,
                    iva=ticket.iva,
                    date=ticket.date,
                    email=ticket.email,
                    location=ticket.location
                ) for ticket in tickets
            ]

    @staticmethod
    def from_tickets_month_to_dto(tickets_by_month: [TicketsMonth]) -> [TicketsMonthResponse]:
        return [
            TicketsMonthResponse(
                month=ticket_month.month,
                num_tickets=ticket_month.num_tickets,
                total=ticket_month.total,
                total_difference=tickets_by_month.total_difference,
                tickets=TicketDTOMapper.tickets_to_dto(ticket_month.tickets),
            )
            for ticket_month in tickets_by_month
        ]
