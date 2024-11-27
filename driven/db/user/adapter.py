from asgiref.sync import sync_to_async
from django.db import transaction

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

    async def update_fcm_token(self, user: User, token: str, platform: str):
        @sync_to_async
        def update_token_sync():
            with transaction.atomic():
                user_dbo = UserDBO.objects.get(email=user.email)
                device, created = user_dbo.devices.get_or_create(device_id=token, platform=platform)
                return created

        try:
            created = await update_token_sync()
            if created:
                print(f'New device created with token: {token}')
            else:
                print(f'Device with token {token} already exists')
        except UserDBO.DoesNotExist:
            raise ValueError(f'User with email {user.email} does not exist')
        except Exception as e:
            raise ValueError(f'Failed to update FCM token: {str(e)}')

