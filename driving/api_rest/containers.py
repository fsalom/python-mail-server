from fastapi import FastAPI

from infrastructure.di.authentication.container import AuthContainer
from infrastructure.di.tickets.container import TicketContainer


def add_containers(app: FastAPI):
    authentication_container = AuthContainer()
    tickets_container = TicketContainer()
    app.authentication_container = authentication_container
    app.tickets_container = tickets_container
