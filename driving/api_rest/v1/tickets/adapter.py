from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from application.ports.driving.tickets_service_port import TicketServicePort
from driving.api_rest.v1.tickets.mapper import TicketDTOMapper
from driving.api_rest.v1.tickets.models import StatsForTicketsResponse
from infrastructure.di.tickets.container import TicketContainer
from application.services.ticket_services import TicketServices
from domain.user import User
from driving.api_rest.security import get_user_or_refuse

ticket_router = APIRouter()


@ticket_router.get('/tickets/all')
@inject
async def me(user: Annotated[User, Depends(get_user_or_refuse)],
             service: TicketServicePort = Depends(Provide[TicketContainer.service]),
             api_mapper: TicketDTOMapper = Depends(Provide[TicketContainer.api_mapper])):
    tickets = await service.get_ticket_for_user(user=user.email)
    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(api_mapper.to_dto(tickets))
        )


@ticket_router.get('/tickets/stats')
@inject
async def stats(user: Annotated[User, Depends(get_user_or_refuse)],
                service: TicketServicePort = Depends(Provide[TicketContainer.service]),
                api_mapper: TicketDTOMapper = Depends(Provide[TicketContainer.api_mapper]),
                start_date: str = Query(..., description="Start date in format YYYY-MM-DD"),
                end_date: str = Query(..., description="End date in format YYYY-MM-DD")):
    date_range = api_mapper.date_str_to_domain(start_date=start_date, end_date=end_date)
    total = await service.get_total_for(user=user.email, date_range=date_range)
    num_tickets = await service.get_number_of_tickets_for(user=user.email, date_range=date_range)
    num_products = await service.get_number_of_products_for(user=user.email, date_range=date_range)
    top_products = await service.get_top_products_for(user=user.email, date_range=date_range, number=3)
    top_products_dto = api_mapper.products_to_dto(top_products)

    return StatsForTicketsResponse(total=total,
                                   num_tickets=num_tickets,
                                   num_products=num_products,
                                   top_products=top_products_dto)


@ticket_router.get('/tickets/stats/all')
@inject
async def stats(user: Annotated[User, Depends(get_user_or_refuse)],
                service: TicketServicePort = Depends(Provide[TicketContainer.service]),
                api_mapper: TicketDTOMapper = Depends(Provide[TicketContainer.api_mapper])):
    total = await service.get_total_for(user=user.email, date_range=None)
    num_tickets = await service.get_number_of_tickets_for(user=user.email, date_range=None)
    num_products = await service.get_number_of_products_for(user=user.email, date_range=None)
    top_products = await service.get_top_products_for(user=user.email, date_range=None, number=3)
    top_products_dto = api_mapper.products_to_dto(top_products)

    return StatsForTicketsResponse(total=total,
                                   num_tickets=num_tickets,
                                   num_products=num_products,
                                   top_products=top_products_dto)


@ticket_router.get('/tickets/populate_tickets_date')
@inject
async def populate(service: TicketServices = Depends(Provide[TicketContainer.service])):
    await service.update_existing_tickets()
    return {"message": "Tickets populated successfully"}
