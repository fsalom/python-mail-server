from abc import ABC, abstractmethod

from domain.tokens import Tokens
from domain.user import User


class AuthServicePort(ABC):
    @abstractmethod
    def login(self, username: str, password: str, client_id: str) -> Tokens | None:
        pass

    @abstractmethod
    def login_from_google_login(self, id_token: str, client_id: str) -> Tokens | None:
        pass

    @abstractmethod
    def login_from_apple_login(self, auth_code: str, client_id: str) -> Tokens | None:
        pass

    @abstractmethod
    def refresh(self, refresh_token: str, client_id: str) -> Tokens | None:
        pass

    @abstractmethod
    def get_user(self, token: str) -> User | None:
        pass

    @abstractmethod
    def logout(self, user: User):
        pass