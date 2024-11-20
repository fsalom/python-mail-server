from abc import ABC, abstractmethod
from typing import List

from domain.notification import Notification


class FirebaseRepositoryPort(ABC):
    @abstractmethod
    def send_single_notification(self, notification: Notification, token: str) -> Notification:
        raise NotImplementedError

    @abstractmethod
    def send_bulk_notification(self, notification: Notification, tokens: List[str]) -> Notification:
        raise NotImplementedError

    @abstractmethod
    def send_single_silent_notification(self, notification: Notification, token: str) -> Notification:
        raise NotImplementedError

    @abstractmethod
    def send_bulk_silent_notification(self, bulk_notification_dto: Notification, tokens: List[str]) -> Notification:
        raise NotImplementedError
