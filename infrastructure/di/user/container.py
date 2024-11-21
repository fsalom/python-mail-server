from dependency_injector import containers, providers

from application.services.user_services import UserServices
from driven.db.user.adapter import UserDBRepositoryAdapter
from driven.db.user.mapper import UserDBMapper
from driving.api_rest.v1.user.mapper import UserDTOMapper


class UserContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    wiring_config = containers.WiringConfiguration(modules=["driving.api_rest.security",
                                                            "driving.api_rest.v1.user.adapter"])
    db_mapper = providers.Factory(
        UserDBMapper
    )

    db_repository = providers.Factory(
        UserDBRepositoryAdapter,
        mapper=db_mapper.provider
    )

    api_mapper = providers.Factory(
        UserDTOMapper
    )

    service = providers.Factory(
        UserServices,
        db_repository=db_repository
    )
