from typing import Annotated

from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from application.ports.driving.user_service_port import UserServicePort
from domain.user import User
from driving.api_rest.security import get_user_or_refuse
from driving.api_rest.v1.user.mapper import UserDTOMapper
from driving.api_rest.v1.user.models import FCMRequest
from infrastructure.di.user.container import UserContainer

user_router = APIRouter()


@user_router.get('/users/me')
async def me(user: Annotated[User, Depends(get_user_or_refuse)],
             api_mapper: UserDTOMapper = Depends(Provide[UserContainer.api_mapper])):
    return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=jsonable_encoder(api_mapper.to_dto(user))
            )


@user_router.patch('/users/me/device')
async def update_fcm(user: Annotated[User, Depends(get_user_or_refuse)],
                     fcm_request: FCMRequest,
                     service: UserServicePort = Depends(Provide[UserContainer.service]),
                     api_mapper: UserDTOMapper = Depends(Provide[UserContainer.api_mapper])):
    await service.update_fcm_token(user, fcm_request.device_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(api_mapper.to_dto(user))
    )
