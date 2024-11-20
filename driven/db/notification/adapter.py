from typing import List

from application.ports.driven.database.notification.notification_repository import NotificationDBRepositoryPort
from domain.device import Device
from domain.notification import Notification
from domain.user import User
from driven.db.notification.mapper import NotificationDBMapper
from driven.db.notification.models import DeviceDBO, NotificationDBO, UserNotificationDBO
from driven.db.user.models import UserDBO


class NotificationDBRepositoryAdapter(NotificationDBRepositoryPort):

    def __init__(self, mapper: NotificationDBMapper):
        self.mapper = mapper

    def create_device(self, device: Device, user: User):
        device_dbo, created = DeviceDBO.objects.get_or_create(
            device_id=device.device_id,
            user_id=user.id,
            platform=device.platform,
        )

    def get_devices(self, user: User) -> List[Device]:
        devices = DeviceDBO.objects.filter(user_id=user.id)
        return [self.mapper.from_device_dbo_to_domain(device) for device in devices]

    def create_notification(self, notification: Notification) -> Notification:
        notification = NotificationDBO.objects.create(
            title=notification.title,
            message=notification.content,
            data=notification.data,
            created_by=notification.created_by
        )

        return self.mapper.from_notification_dbo_to_domain(notification)

    def add_notification_to_user(self, notification: Notification, user: User):
        notification = self.create_notification(notification)
        notification_dbo = NotificationDBO.objects.get(id=notification.id)
        user_dbo = UserDBO.objects.get(id=user.id)
        notification_user = UserNotificationDBO.objects.create(
            notification=notification_dbo,
            user=user_dbo,
        )
