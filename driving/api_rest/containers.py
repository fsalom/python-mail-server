from fastapi import FastAPI

from infrastructure.di.authentication.container import AuthContainer
from infrastructure.di.tickets.container import TicketContainer
from infrastructure.di.user.container import UserContainer


def add_containers(app: FastAPI):
    authentication_container = AuthContainer()
    tickets_container = TicketContainer()
    user_container = UserContainer()
    app.authentication_container = authentication_container
    app.tickets_container = tickets_container
    app.user_container = user_container
