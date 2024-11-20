from domain.user import User
from driven.db.user.models import UserDBO


class UserDBMapper:
    @staticmethod
    def from_dbo_to_domain(user_dbo: UserDBO) -> User:
        return User(
            id=user_dbo.id,
            email=user_dbo.email
        )
