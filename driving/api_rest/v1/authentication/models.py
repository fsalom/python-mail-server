from pydantic import BaseModel


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str
    scope: str


class AuthenticationRequest(BaseModel):
    username: str
    password: str
    client_id: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "",
                    "password": "",
                    "client_id": ""
                }
            ]
        }
    }


class AuthRefreshRequest(BaseModel):
    refresh_token: str
    client_id: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "refresh_token": "",
                    "client_id": ""
                }
            ]
        }
    }


class AuthGoogleRequest(BaseModel):
    client_id: str
    id_token: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "client_id": "",
                    "id_token": ""
                }
            ]
        }
    }


class AuthAppleRequest(BaseModel):
    client_id: str
    auth_code: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "client_id": "",
                    "auth_code": ""
                }
            ]
        }
    }