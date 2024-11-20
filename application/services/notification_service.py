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

    def send_single_notification(self, notification: Notification, token: str):
        notification = self.notification_db.create_notification(notification)
        self.firebase.send_single_notification(notification, token)

    def send_single_silent_notification(self, notification: Notification, token: str):
        notification = self.create_notification(notification)
        self.firebase.send_single_silent_notification(notification, token)

    def send_bulk_notification(self, notification: Notification, tokens: List[str]) -> Notification:
        notification = self.create_notification(notification)
        self.firebase.send_bulk_notification(notification, tokens)
        return notification

    def send_bulk_silent_notification(self, notification: Notification, tokens: List[str]) -> Notification:
        notification = self.create_notification(notification)
        self.firebase.send_bulk_silent_notification(notification, tokens)
        return notification
