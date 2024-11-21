from abc import ABC, abstractmethod

from domain.user import User


class UserDBRepositoryPort(ABC):
    @abstractmethod
    def get(self, email: str) -> User:
        pass

    @abstractmethod
    def get_or_create_user_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    def update_fcm_token(self, user: User, token: str, platform: str):
        pass
