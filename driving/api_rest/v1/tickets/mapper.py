from domain.date_range import DateRange
from domain.product import Product
from domain.ticket import Ticket
from driving.api_rest.v1.tickets.models import AllTicketsResponse, TicketResponse, ProductResponse


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
