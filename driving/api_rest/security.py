from typing import Annotated
from asgiref.sync import sync_to_async
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from application.ports.driving.authentication_service_port import AuthServicePort
from infrastructure.di.authentication.container import AuthContainer


@inject
async def get_user_or_refuse(token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))],
                             authentication_service: AuthServicePort
                             = Depends(Provide[AuthContainer.service])):
    user = await sync_to_async(authentication_service.get_user)(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return user
