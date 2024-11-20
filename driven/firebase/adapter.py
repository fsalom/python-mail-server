from typing import List

from firebase_admin import messaging

from application.ports.driven.firebase.repository import FirebaseRepositoryPort
from domain.notification import Notification


class FirebaseRepositoryAdapter(FirebaseRepositoryPort):
    def send_single_notification(self, notification: Notification, device_id: str) -> Notification:
        message = messaging.Message(
            notification=messaging.Notification(
                title=notification.title,
                body=notification.content,
            ),
            token=notification.device_id,
        )
        if notification.data:
            message.data = notification.data
        messaging.send(message)
        return notification

    def send_bulk_notification(self, notification: Notification, device_ids: List[str]) -> Notification:
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=notification.title,
                body=notification.content,
            ),
            tokens=device_ids,
        )
        if notification.data:
            message.data = notification.data
        messaging.send_each_for_multicast(message)
        return notification

    def send_single_silent_notification(self, notification: Notification, device_id: str) -> Notification:
        message = messaging.Message(
            token=device_id,
        )
        if notification.data:
            message.data = notification.data
        messaging.send(message)
        return notification

    def send_bulk_silent_notification(self, notification: Notification, device_ids: List[str]) -> Notification:
        message = messaging.MulticastMessage(
            tokens=device_ids,
        )
        if notification.data:
            message.data = notification.data
        messaging.send_each_for_multicast(message)
        return notification
