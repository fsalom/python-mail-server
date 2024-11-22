from typing import List

from application.ports.driven.database.notification.notification_repository import NotificationDBRepositoryPort
from application.ports.driven.firebase.repository import FirebaseRepositoryPort
from application.ports.driving.notification_service_port import NotificationServicePort
from domain.device import Device
from domain.notification import Notification
from domain.user import User


class NotificationService(NotificationServicePort):
    def __init__(
        self,
        notification_db: NotificationDBRepositoryPort,
        firebase: FirebaseRepositoryPort,
    ):
        self.notification_db = notification_db
        self.firebase = firebase

    def create_device(self, device: Device, user: User = None):
        self.notification_db.create_device(device, user)

    def create_notification(self, notification: Notification) -> Notification:
        return self.notification_db.create_notification(notification)

    def get_devices(self, user: User) -> List[Device]:
        return self.notification_db.get_devices(user=user)

    def send_single_notification(self, notification: Notification, token: str):
        notification = self.notification_db.create_notification(notification)
        updated_notification = self.firebase.send_single_notification(notification, token)
        self._remove_invalid_device_ids(updated_notification.invalid_device_ids)

    def send_single_silent_notification(self, notification: Notification, token: str):
        notification = self.create_notification(notification)
        updated_notification = self.firebase.send_single_silent_notification(notification, token)
        self._remove_invalid_device_ids(updated_notification.invalid_device_ids)

    def send_bulk_notification(self, notification: Notification, tokens: List[str]) -> Notification:
        notification = self.create_notification(notification)
        updated_notification = self.firebase.send_bulk_notification(notification, tokens)
        self._remove_invalid_device_ids(updated_notification.invalid_device_ids)
        return notification

    def send_bulk_silent_notification(self, notification: Notification, tokens: List[str]) -> Notification:
        notification = self.create_notification(notification)
        updated_notification = self.firebase.send_bulk_silent_notification(notification, tokens)
        self._remove_invalid_device_ids(updated_notification.invalid_device_ids)
        return notification

    def _remove_invalid_device_ids(self, devices_ids: List[str]):
        if devices_ids is None:
            return
        for device_id in devices_ids:
            self.notification_db.remove_device(device_id)
