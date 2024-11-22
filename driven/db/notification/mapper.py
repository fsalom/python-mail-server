from domain.device import Device
from domain.notification import Notification
from driven.db.notification.models import DeviceDBO, NotificationDBO
from driven.db.user.mapper import UserDBMapper


class NotificationDBMapper:
    def __init__(self, user_mapper: UserDBMapper):
        self.user_mapper = user_mapper

    @staticmethod
    def from_device_dbo_to_domain(device_dbo: DeviceDBO) -> Device:
        return Device(
            device_id=device_dbo.device_id,
            user_id=device_dbo.user_id,
            platform=device_dbo.platform,
        )

    @staticmethod
    def from_device_domain_to_dbo(device: Device) -> DeviceDBO:
        return DeviceDBO(
            device_id=device.device_id,
            user_id=device.user_id,
            platform=device.platform
        )

    def from_notification_dbo_to_domain(self, notification_dbo: NotificationDBO) -> Notification:
        return Notification(
            id=notification_dbo.id,
            title=notification_dbo.title,
            content=notification_dbo.message,
            data=notification_dbo.data,
            created_by=self.user_mapper.from_dbo_to_domain(notification_dbo.created_by),
        )
