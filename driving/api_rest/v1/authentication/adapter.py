from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from application.ports.driving.authentication_service_port import AuthenticationServicePort
from domain.user import User
from driving.api_rest.security import get_user_or_refuse
from driving.api_rest.v1.authentication.mapper import AuthenticationDTOMapper
from driving.api_rest.v1.authentication.models import AuthenticationResponse, AuthenticationRequest, \
    AuthenticationRefreshRequest
from infrastructure.di.authentication.container import AuthenticationContainer

auth_router = APIRouter()


@auth_router.post('/auth/login', status_code=200, response_model=AuthenticationResponse)
@inject
def auth(authentication_request: AuthenticationRequest,
         authentication_service: AuthenticationServicePort = Depends(
             Provide[AuthenticationContainer.service]
         ),
         api_rest_mapper: AuthenticationDTOMapper = Depends(
             AuthenticationDTOMapper
         )
         ) -> JSONResponse:
    tokens = authentication_service.login(username=authentication_request.username,
                                          password=authentication_request.password,
                                          client_id=authentication_request.client_id)
    if tokens is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": "Not authenticated"})

    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(api_rest_mapper.to_dto(tokens=tokens)))


@auth_router.post('/auth/refresh', status_code=200, response_model=AuthenticationResponse)
@inject
def auth_refresh(authentication_request: AuthenticationRefreshRequest,
                 authentication_service: AuthenticationServicePort = Depends(
                     Provide[AuthenticationContainer.service]
                 ),
                 api_rest_mapper: AuthenticationDTOMapper = Depends(
                     AuthenticationDTOMapper
                 )
                 ) -> JSONResponse:
    tokens = authentication_service.refresh(refresh_token=authentication_request.refresh_token,
                                            client_id=authentication_request.client_id)
    if tokens is None:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"message": "Not authenticated"})

    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(api_rest_mapper.to_dto(tokens=tokens)))


@auth_router.post('/auth/logout', status_code=200, response_model=AuthenticationResponse)
@inject
def auth_logout(user: Annotated[User, Depends(get_user_or_refuse)],
                authentication_service: AuthenticationServicePort = Depends(
                    Provide[AuthenticationContainer.service]
                )
                ) -> JSONResponse:

    if not authentication_service.logout(user=user):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": "Something went wrong"})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={})
