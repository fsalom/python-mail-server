from asgiref.sync import sync_to_async

from application.ports.driven.apple.apple_repository_port import AppleRepositoryPort
from application.ports.driven.database.authentication.db_repository import AuthenticationDBRepositoryPort
from application.ports.driven.database.user.db_repository import UserDBRepositoryPort
from application.ports.driven.google.google_repository import GoogleRepositoryPort
from application.ports.driving.authentication_service_port import AuthServicePort
from domain.tokens import Tokens
from domain.user import User


class AuthServices(AuthServicePort):

    def __init__(self,
                 db_repository: AuthenticationDBRepositoryPort,
                 google_repository: GoogleRepositoryPort,
                 apple_repository: AppleRepositoryPort,
                 user_db_repository: UserDBRepositoryPort
                 ):
        self.db_repository = db_repository
        self.google_repository = google_repository
        self.apple_repository = apple_repository
        self.user_db_repository = user_db_repository

    def refresh(self, refresh_token: str, client_id: str) -> Tokens | None:
        return self.db_repository.refresh(refresh_token, client_id)

    def login(self, username: str, password: str, client_id: str) -> Tokens | None:
        return self.db_repository.login(username, password, client_id)

    def login_from_google_login(self, id_token: str, client_id: str) -> Tokens | None:
        google_info = self.google_repository.validate_token(id_token)
        if google_info:
            user = self.user_db_repository.get_or_create_user_by_email(google_info.email)
            return self.db_repository.login_from_google_info(user, client_id)
        else:
            return None

    def login_from_apple_login(self, auth_code: str, client_id: str) -> Tokens | None:
        apple_info = self.apple_repository.validate_token(auth_code)
        if apple_info:
            user = self.user_db_repository.get_or_create_user_by_email(apple_info.email)
            return self.db_repository.login_from_apple_info(user, client_id)
        else:
            return None

    def logout(self, user: User):
        return self.db_repository.logout(user)

    def get_user(self, token: str) -> User | None:
        user = self.db_repository.get_user(token)
        return user
