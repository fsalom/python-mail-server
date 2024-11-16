import os
from datetime import timedelta
import requests
from django.utils import timezone
import jwt
from application.ports.driven.apple.apple_repository_port import AppleRepositoryPort
from domain.apple_info import AppleInfo
from driven.apple.mapper import AppleInfoMapper
from infrastructure.django import settings


class AppleRepositoryAdapter(AppleRepositoryPort):
    """
    https://medium.com/@aamishbaloch/sign-in-with-apple-in-your-django-python-backend-b501daa835a9
    """

    def validate_token(self, auth_code: str) -> AppleInfo:
        headers = {"content-type": "application/x-www-form-urlencoded"}

        data = {
            "client_id": os.environ['APPLE_CLIENT_ID'],
            "client_secret": self._create_client_secret(),
            "code": auth_code,
            "grant_type": "authorization_code",
        }

        apple_info = requests.post(
            'https://appleid.apple.com/auth/token', data=data, headers=headers
        )
        if apple_info.status_code != 200:
            raise ValueError('Invalid Apple token.')
        response = apple_info.json()
        return self._decode_id_token(response['id_token'])

    def _create_client_secret(self) -> str:
        headers = {'kid': os.environ['APPLE_KEY_ID']}

        payload = {
            'iss': os.environ['APPLE_DEVELOPER_TEAM_ID'],
            'iat': timezone.localtime(),
            'exp': timezone.localtime() + timedelta(days=180),
            'aud': 'https://appleid.apple.com',
            'sub': os.environ['APPLE_CLIENT_ID'],
        }

        client_secret = jwt.encode(
            payload,
            open(settings.APPLE_PRIVATE_KEY).read(),
            algorithm='ES256',
            headers=headers,
        )
        return client_secret

    def _decode_id_token(self, apple_id_token: str) -> AppleInfo:
        apple_info = jwt.decode(
            apple_id_token,
            '',
            verify=False,
            options={"verify_signature": False},
            algorithms=["HS256"],
        )
        return AppleInfoMapper.from_json_to_entity(apple_info)
