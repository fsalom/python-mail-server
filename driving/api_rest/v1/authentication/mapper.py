from domain.tokens import Tokens
from driving.api_rest.v1.authentication.models import AuthResponse


class AuthDTOMapper:
    @staticmethod
    def to_dto(tokens: Tokens) -> AuthResponse:
        return AuthResponse(access_token=tokens.access_token,
                            refresh_token=tokens.refresh_token,
                            expires_in=tokens.expires_in,
                            token_type=tokens.token_type,
                            scope=tokens.scope)
