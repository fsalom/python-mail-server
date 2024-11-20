from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from application.ports.driving.notification_service_port import FCMServicePort
from domain.user import User
from driving.api_rest.security import get_user_or_refuse
from driving.api_rest.v1.notification.mapper import NotificationAPIMapper
from driving.api_rest.v1.notification.models import DeviceRequest, NotificationRequest
from infrastructure.di.notification.container import NotificationContainer

fcm_router = APIRouter()


@fcm_router.get('/notification/device/create')
@inject
async def create_device(device_request: DeviceRequest,
                        user: Annotated[User, Depends(get_user_or_refuse)],
                        service: FCMServicePort = Depends(Provide[NotificationContainer.service]),
                        mapper: NotificationAPIMapper = Depends(Provide[NotificationContainer.api_mapper])):
    device = mapper.from_device_dto_to_domain(device_request)
    service.create_device(device, user)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message: Device created"},
    )


@fcm_router.post('/notification/create')
@inject
async def create_notification(notification_request: NotificationRequest,
                              service: FCMServicePort = Depends(Provide[NotificationContainer.service]),
                              mapper: NotificationAPIMapper = Depends(
                                  Provide[NotificationContainer.api_mapper])):
    notification = mapper.from_notification_dto_to_domain(notification_request)
    service.create_notification(notification)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message: Device created"},
    )


@fcm_router.post('/notification/send')
@inject
async def send_notification(notification_request: NotificationRequest,
                            user: Annotated[User, Depends(get_user_or_refuse)],
                            service: FCMServicePort = Depends(Provide[NotificationContainer.service]),
                            mapper: NotificationAPIMapper = Depends(Provide[NotificationContainer.api_mapper])):
    notification = mapper.from_notification_dto_to_domain(notification_request)
    service.send_single_notification(notification, user)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=None
    )
