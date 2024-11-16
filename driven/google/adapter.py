import requests

from application.ports.driven.google.google_repository import GoogleRepositoryPort
from domain.google_info import GoogleInfo
from driven.google.mapper import GoogleInfoMapper


class GoogleRepositoryAdapter(GoogleRepositoryPort):
    def validate_token(self, id_token: str) -> GoogleInfo:
        google_info = requests.get(
            'https://www.googleapis.com/oauth2/v3/tokeninfo',
            params={'id_token': id_token},
        )
        if google_info.status_code != 200:
            raise ValueError('Invalid Google token.')
        return GoogleInfoMapper.from_json_to_entity(google_info.json())