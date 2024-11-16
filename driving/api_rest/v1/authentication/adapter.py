from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from application.ports.driving.authentication_service_port import AuthServicePort
from domain.user import User
from driving.api_rest.security import get_user_or_refuse
from driving.api_rest.v1.authentication.mapper import AuthDTOMapper
from driving.api_rest.v1.authentication.models import AuthResponse, AuthenticationRequest, \
    AuthRefreshRequest, AuthGoogleRequest, AuthAppleRequest
from infrastructure.di.authentication.container import AuthContainer

auth_router = APIRouter()


@auth_router.post('/auth/login', status_code=200, response_model=AuthResponse)
@inject
def auth(request: AuthenticationRequest,
         service: AuthServicePort = Depends(Provide[AuthContainer.service]),
         mapper: AuthDTOMapper = Depends(AuthDTOMapper)) -> JSONResponse:

    tokens = service.login(username=request.username,
                           password=request.password,
                           client_id=request.client_id)
    if tokens is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": "Not authenticated"})

    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(mapper.to_dto(tokens=tokens)))


@auth_router.post('/auth/refresh', status_code=200, response_model=AuthResponse)
@inject
def auth_refresh(request: AuthRefreshRequest,
                 service: AuthServicePort = Depends(Provide[AuthContainer.service]),
                 mapper: AuthDTOMapper = Depends(AuthDTOMapper)) -> JSONResponse:

    tokens = service.refresh(refresh_token=request.refresh_token,
                             client_id=request.client_id)
    if tokens is None:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"message": "Not authenticated"})

    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(mapper.to_dto(tokens=tokens)))


@auth_router.post('/auth/logout', status_code=200, response_model=AuthResponse)
@inject
def auth_logout(user: Annotated[User, Depends(get_user_or_refuse)],
                service: AuthServicePort = Depends(Provide[AuthContainer.service])) -> JSONResponse:

    if not service.logout(user=user):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": "Something went wrong"})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={})


@auth_router.post('/auth/google', status_code=200, response_model=AuthResponse)
@inject
def google_login(request: AuthGoogleRequest,
                 service: AuthServicePort = Depends(Provide[AuthContainer.service]),
                 mapper: AuthDTOMapper = Depends(AuthDTOMapper)) -> JSONResponse:

    tokens = service.login_from_google_login(request.id_token, request.client_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(mapper.to_dto(tokens=tokens))
    )


@auth_router.post('/auth/apple', status_code=200, response_model=AuthResponse)
@inject
def google_apple(request: AuthAppleRequest,
                 service: AuthServicePort = Depends(Provide[AuthContainer.service]),
                 mapper: AuthDTOMapper = Depends(AuthDTOMapper)) -> JSONResponse:

    tokens = service.login_from_apple_login(request.auth_code, request.client_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(mapper.to_dto(tokens=tokens))
    )
