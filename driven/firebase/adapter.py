from typing import List

from firebase_admin import messaging
from firebase_admin.messaging import Message, MulticastMessage

from application.ports.driven.firebase.repository import FirebaseRepositoryPort
from domain.notification import Notification


class FirebaseRepositoryAdapter(FirebaseRepositoryPort):
    def send_single_notification(self, notification: Notification, device_id: str) -> Notification:
        message = messaging.Message(
            notification=messaging.Notification(
                title=notification.title,
                body=notification.content,
            ),
            token=device_id,
        )
        return self._send_single(message=message, notification=notification, device_id=device_id)

    def send_bulk_notification(self, notification: Notification, device_ids: List[str]) -> Notification:
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=notification.title,
                body=notification.content,
            ),
            tokens=device_ids,
        )
        return self._send_bulk(message=message, notification=notification, device_ids=device_ids)

    def send_single_silent_notification(self, notification: Notification, device_id: str) -> Notification:
        message = messaging.Message(
            token=device_id,
        )
        return self._send_single(message=message, notification=notification, device_id=device_id)

    def send_bulk_silent_notification(self, notification: Notification, device_ids: List[str]) -> Notification:
        message = messaging.MulticastMessage(
            tokens=device_ids,
        )
        return self._send_bulk(message=message, notification=notification, device_ids=device_ids)

    @staticmethod
    def _send_single(message: Message, notification: Notification, device_id: str) -> Notification:
        if notification.data:
            message.data = notification.data
        try:
            response = messaging.send(message)
        except messaging.UnregisteredError:
            print(f"Device token {device_id} is no longer valid and should be removed.")
            notification.invalid_device_ids.append(device_id)
        except messaging.QuotaExceededError as e:
            print(f"Invalid token {device_id}: {e}")
        except Exception as e:
            print(f"Failed to send message to {device_id}: {e}")
        return notification

    @staticmethod
    def _send_bulk(message: MulticastMessage, notification: Notification, device_ids: List[str]) -> Notification:
        if notification.data:
            message.data = notification.data

        batch_response = messaging.send_each_for_multicast(message)
        invalid_device_ids = []

        for idx, response in enumerate(batch_response.responses):
            if not response.success:
                failed_token = device_ids[idx]
                exception = response.exception
                if isinstance(exception, messaging.UnregisteredError):
                    invalid_device_ids.append(failed_token)
                else:
                    print(f"Failed to send to {failed_token}: {exception}")

        notification.sent_to_device_ids = device_ids
        notification.invalid_device_ids = invalid_device_ids
        return notification
