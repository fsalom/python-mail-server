from abc import ABC, abstractmethod

from domain.apple_info import AppleInfo
from domain.google_info import GoogleInfo
from domain.tokens import Tokens
from domain.user import User


class AuthenticationDBRepositoryPort(ABC):
    @abstractmethod
    def login(self, username: str, password: str, client_id: str) -> Tokens | None:
        pass

    @abstractmethod
    def login_from_google_info(self, info: GoogleInfo, client_id: str) -> Tokens | None:
        pass

    @abstractmethod
    def login_from_apple_info(self, info: AppleInfo, client_id: str) -> Tokens | None:
        pass

    @abstractmethod
    def logout(self, user: User) -> bool:
        pass

    @abstractmethod
    def get_user(self, token: str) -> User | None:
        pass

    @abstractmethod
    def refresh(self, refresh_token: str, client_id: str) -> Tokens | None:
        pass
