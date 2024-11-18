from fastapi import FastAPI

from driving.api_rest.health.adapter import health_router
from driving.api_rest.v1.authentication.adapter import auth_router
from driving.api_rest.v1.tickets.adapter import ticket_router
from driving.api_rest.v1.user.adapter import user_router


def add_routers(app: FastAPI):
    app.include_router(health_router, prefix='/api')
    # v1
    app.include_router(auth_router, prefix='/api/v1')
    app.include_router(user_router, prefix='/api/v1')
    app.include_router(ticket_router, prefix='/api/v1')
