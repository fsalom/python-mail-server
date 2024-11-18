from domain.product import Product
from domain.ticket import Ticket
from driven.db.product.models import ProductDBO, ProductPriceHistoryDBO
from driven.db.store.models import StoreDBO
from driven.db.ticket.models import TicketDBO, TicketProductDBO
from driven.db.user.models import UserDBO


class TicketDBMapper:
    @staticmethod
    def to_domain(tickets_dbo_list: [TicketDBO]) -> [Ticket]:
        tickets = []
        for ticket_dbo in tickets_dbo_list:
            products = [
                TicketDBMapper.ticket_product_dbo_to_domain(ticket_product_dbo)
                for ticket_product_dbo in ticket_dbo.ticket_products.all()
            ]
            tickets.append(
                Ticket(
                    id_ticket=ticket_dbo.id_ticket,
                    products=products,
                    total=ticket_dbo.total,
                    iva=0.0,
                    date=str(ticket_dbo.date_raw),
                    email=ticket_dbo.email.email,
                    location=ticket_dbo.location.location_info,
                )
            )
        return tickets

    @staticmethod
    def ticket_product_dbo_to_domain(product_of_ticket: TicketProductDBO):
        return Product(
            name=product_of_ticket.product.name,
            quantity=product_of_ticket.quantity,
            price_per_unit=product_of_ticket.history_price.price_per_unit,
            price=product_of_ticket.history_price.price,
            weight=None
        )

    @staticmethod
    def map_store(ticket: Ticket) -> StoreDBO:
        store_dbo, _ = StoreDBO.objects.get_or_create(
            location_info=ticket.location
        )
        return store_dbo

    @staticmethod
    def map_user(ticket: Ticket) -> UserDBO:
        user_dbo, _ = UserDBO.objects.get_or_create(
            email=ticket.email,
            username=ticket.email
        )
        return user_dbo

    @staticmethod
    def map_product(product: Product, date: str) -> (ProductDBO, ProductPriceHistoryDBO):
        product_dbo, _ = ProductDBO.objects.get_or_create(
            name=product.name
        )
        product_history_price, _ = ProductPriceHistoryDBO.objects.get_or_create(
            product=product_dbo,
            date_raw=date,
            price=product.price,
            price_per_unit=product.price_per_unit
        )
        return product_dbo, product_history_price

    @staticmethod
    def map_ticket(ticket: Ticket, store_dbo: StoreDBO, user_dbo: UserDBO) -> TicketDBO:
        ticket_dbo, _ = TicketDBO.objects.get_or_create(
            date_raw=ticket.date,
            location=store_dbo,
            email=user_dbo,
            total=ticket.total,
            id_ticket=ticket.id
        )
        return ticket_dbo

    @staticmethod
    def map_products_of_ticket(ticket: TicketDBO, products: [Product], date: str) -> [ProductDBO]:
        products_dbo = []
        for product in products:
            product_dbo, product_history_price = TicketDBMapper.map_product(product, date)

            TicketProductDBO.objects.create(
                ticket=ticket,
                product=product_dbo,
                quantity=product.quantity,
                history_price=product_history_price,
                units=product.price_per_unit
            )

            products_dbo.append(product_dbo)
        return products_dbo
