from dependency_injector import containers, providers
from fastapi.security import OAuth2PasswordBearer

from application.services.authentication_services import AuthServices
from driven.apple.adapter import AppleRepositoryAdapter
from driven.db.authentication.adapter import AuthenticationDBRepositoryAdapter
from driven.db.user.adapter import UserDBRepositoryAdapter
from driven.db.user.mapper import UserDBMapper
from driven.google.adapter import GoogleRepositoryAdapter


class AuthContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    wiring_config = containers.WiringConfiguration(modules=["driving.api_rest.security",
                                                            "driving.api_rest.v1.authentication.adapter"])
    db_repository = providers.Factory(AuthenticationDBRepositoryAdapter)
    user_db_repository = providers.Factory(
        UserDBRepositoryAdapter,
        mapper=UserDBMapper()
    )
    google_repository = providers.Factory(GoogleRepositoryAdapter)
    apple_repository = providers.Factory(AppleRepositoryAdapter)
    oauth2_scheme = providers.Singleton(OAuth2PasswordBearer, tokenUrl="token")

    service = providers.Factory(
        AuthServices,
        db_repository=db_repository,
        google_repository=google_repository,
        apple_repository=apple_repository,
        user_db_repository=user_db_repository
    )
