from pydantic import BaseModel


class UserResponse(BaseModel):
    username: str
    email: str

    class Config:
        from_attributes = True


class UserRequest(BaseModel):
    email: str

    class Config:
        from_attributes = True


class FCMRequest(BaseModel):
    device_id: str

    class Config:
        from_attributes = True
