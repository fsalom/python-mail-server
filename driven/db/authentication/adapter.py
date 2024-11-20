from datetime import timedelta

from django.contrib.auth import authenticate
from django.utils import timezone
from oauth2_provider.models import RefreshToken, Application, AccessToken
from oauth2_provider.settings import oauth2_settings
from application.ports.driven.database.authentication.db_repository import AuthenticationDBRepositoryPort
from domain.google_info import GoogleInfo
from domain.tokens import Tokens
from domain.user import User
from driven.db.user.models import UserDBO


class AuthenticationDBRepositoryAdapter(AuthenticationDBRepositoryPort):

    @staticmethod
    def get_application(client_id) -> Application | None:
        try:
            application = Application.objects.get(client_id=client_id)
            return application
        except Application.DoesNotExist:
            return None

    @staticmethod
    def get_expire_time() -> timedelta:
        now = timezone.now()
        expires = now + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
        return expires

    def logout(self, user: User) -> bool:
        try:
            refresh_token = RefreshToken.objects.get(user=user)
        except RefreshToken.DoesNotExist:
            return False
        refresh_token.revoke()
        return True

    def refresh(self, refresh_token: str, client_id: str) -> Tokens | None:
        if refresh_token is None:
            return None
        application = self.get_application(client_id)
        if application is None:
            return None

        try:
            refresh_token = RefreshToken.objects.get(token=refresh_token)
        except RefreshToken.DoesNotExist:
            return None

        access_token = AccessToken.objects.create(
            user=refresh_token.user,
            application=application,
            expires=self.get_expire_time(),
            token=oauth2_settings.ACCESS_TOKEN_GENERATOR(),
            scope="read write"
        )

        refresh_token.access_token = access_token
        refresh_token.save()

        return Tokens(
            access_token=access_token.token,
            refresh_token=refresh_token.token,
            expires_in=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
            token_type='Bearer',
            scope=access_token.scope
        )

    def login(self, username: str, password: str, client_id: str) -> Tokens | None:
        user = authenticate(username=username, password=password)
        if user is None:
            return None

        application = self.get_application(client_id)
        if application is None:
            return None

        return self.get_token_for_user(user, application)

    def login_from_google_info(self, user: User, client_id: str) -> Tokens | None:
        if user is None:
            return None

        application = self.get_application(client_id)

        return self.get_token_for_user(user, application)

    def login_from_apple_info(self, user: User, client_id: str) -> Tokens | None:
        if user is None:
            return None

        application = self.get_application(client_id)

        return self.get_token_for_user(user, application)

    def get_user(self, token: str) -> User | None:
        try:
            access_token = AccessToken.objects.filter(token=token, expires__gt=timezone.now()).first()
            if access_token is None:
                return None
            user = access_token.user
            return user
        except Exception as e:
            return None

    def get_token_for_user(self, user: User, application: Application) -> Tokens:
        user_dbo = UserDBO.objects.get(id=user.id)
        access_token = AccessToken.objects.create(
            user=user_dbo,
            application=application,
            expires=self.get_expire_time(),
            token=oauth2_settings.ACCESS_TOKEN_GENERATOR(),
            scope="read write"
        )

        refresh_token = RefreshToken.objects.create(
            user=user_dbo,
            token=oauth2_settings.REFRESH_TOKEN_GENERATOR(),
            application=application,
            access_token=access_token,
        )

        return Tokens(
            access_token=access_token.token,
            refresh_token=refresh_token.token,
            expires_in=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
            token_type='Bearer',
            scope=access_token.scope
        )
