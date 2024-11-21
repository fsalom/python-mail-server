from abc import ABC, abstractmethod
from domain.user import User


class UserServicePort(ABC):
    @abstractmethod
    async def get(self, email: str) -> User:
        pass

    @abstractmethod
    async def update_fcm_token(self, user: User, token: str, platform: str):
        pass
