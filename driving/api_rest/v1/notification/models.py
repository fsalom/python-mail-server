from typing import Any, Dict, List, Optional
from pydantic import Field, StringConstraints, BaseModel
from typing_extensions import Annotated, Literal

FirebaseDeviceId = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        pattern=r'^[a-zA-Z0-9-_]{22}:[a-zA-Z0-9-_]+$',
        min_length=163,
        max_length=163,
    ),
]

PlatformDevice = Literal['ios', 'android']


class DeviceRequest(BaseModel):
    device_id: FirebaseDeviceId
    platform: PlatformDevice

    model_config = {
        "json_schema_extra": {
            "device": [
                {
                    "device_id": "asdfasf",
                    "platform": "ios"
                }
            ]
        }
    }


class NotificationRequest(BaseModel):
    id: Optional[int] = Field(default=None)
    title: str
    content: str
    data: Optional[Dict[str, Any]] = Field(default=None)

    model_config = {
        "json_schema_extra": {
            "notification": [
                {
                    "device_id": "asdfasf",
                    "id": "",
                    "title": "example",
                    "content": "example",
                    "data": "ios"
                }
            ]
        }
    }


class NotificationResponse(BaseModel):
    id: int
    title: str
    content: str

    model_config = {
        "json_schema_extra": {
            "notification": [
                {
                    "id": 1,
                    "title": "title example",
                    "content": "example"
                }
            ]
        }
    }
