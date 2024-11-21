from application.ports.driven.database.user.db_repository import UserDBRepositoryPort
from application.ports.driving.user_service_port import UserServicePort
from domain.user import User


class UserServices(UserServicePort):
    def __init__(self, db_repository: UserDBRepositoryPort):
        self.db_repository = db_repository

    async def get(self, email: str) -> User:
        return self.db_repository.get(email)

    async def update_fcm_token(self, user: User, token: str, platform: str):
        return await self.db_repository.update_fcm_token(user, token, platform)
