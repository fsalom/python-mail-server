from dependency_injector import containers, providers

from application.services.ticket_services import TicketServices
from driven.db.ticket.adapter import TicketDBRepositoryAdapter
from driven.db.ticket.mapper import TicketDBMapper
from driving.api_rest.v1.tickets.mapper import TicketDTOMapper


class TicketContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    wiring_config = containers.WiringConfiguration(modules=["driving.api_rest.v1.tickets.adapter"])

    db_mapper = providers.Factory(
        TicketDBMapper
    )

    db_repository = providers.Factory(
        TicketDBRepositoryAdapter,
        mapper=db_mapper,
    )

    service = providers.Factory(
        TicketServices,
        db_repository=db_repository
    )

    api_mapper = providers.Factory(
        TicketDTOMapper
    )
