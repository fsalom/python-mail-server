from domain.device import Device
from domain.notification import Notification
from driving.api_rest.v1.notification.models import DeviceRequest, NotificationRequest, NotificationResponse


class NotificationAPIMapper:
    @staticmethod
    def from_device_dto_to_domain(dto: DeviceRequest) -> Device:
        return Device(
            device_id=dto.device_id,
            platform_id=dto.platform,
            user_id=dto.user_id
        )

    @staticmethod
    def from_notification_dto_to_domain(dto: NotificationRequest) -> Notification:
        return Notification(
            content=dto.content,
            title=dto.title,
            data=dto.data,
        )

    @staticmethod
    def from_domain_to_notification_dto(domain: Notification) -> NotificationResponse:
        return NotificationResponse(
            id=domain.id,
            content=domain.content,
            title=domain.title,
            data=domain.data,
        )
