from domain.device import Device
from domain.notification import Notification
from driven.db.notification.models import DeviceDBO, NotificationDBO


class NotificationDBMapper:
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

    @staticmethod
    def from_notification_dbo_to_domain(notification_dbo: NotificationDBO) -> Notification:
        return Notification(
            id=notification_dbo.id,
            title=notification_dbo.title,
            content=notification_dbo.message,
            data=notification_dbo.data,
        )

    @staticmethod
    def from_entity_to_model(notification: Notification) -> NotificationDBO:
        return NotificationDBO(
            device_id=notification.device_id,
            content=notification.content
        )
