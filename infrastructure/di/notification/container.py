from dependency_injector import containers, providers

from application.services.notification_service import NotificationService
from driven.db.notification.adapter import NotificationDBRepositoryAdapter
from driven.db.notification.mapper import NotificationDBMapper
from driven.firebase.adapter import FirebaseRepositoryAdapter
from driving.api_rest.v1.notification.mapper import NotificationAPIMapper


class NotificationContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    wiring_config = containers.WiringConfiguration(modules=["driving.api_rest.security",
                                                            "driving.api_rest.v1.notification.adapter"])
    db_repository = providers.Factory(
        NotificationDBRepositoryAdapter,
        mapper=NotificationDBMapper(),
    )

    firebase_repository = providers.Factory(FirebaseRepositoryAdapter)

    service = providers.Factory(
        NotificationService,
        db_repository=db_repository,
        firebase_repository=firebase_repository,
    )

    api_mapper = providers.Factory(
        NotificationAPIMapper
    )