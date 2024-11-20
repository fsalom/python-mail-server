from application.ports.driven.database.user.db_repository import UserDBRepositoryPort
from domain.user import User
from driven.db.user.mapper import UserDBMapper
from driven.db.user.models import UserDBO


class UserDBRepositoryAdapter(UserDBRepositoryPort):
    def __init__(self, mapper: UserDBMapper):
        self.mapper = mapper

    def get(self, email: str) -> User:
        try:
            user = UserDBO.objects.get(email=email)
            return self.mapper.from_dbo_to_domain(user)
        except Exception as e:
            return None

    def get_or_create_user_by_email(self, email: str) -> User | None:
        try:
            user, _ = UserDBO.objects.get_or_create(email=email)
            return self.mapper.from_dbo_to_domain(user)
        except Exception as e:
            return None
