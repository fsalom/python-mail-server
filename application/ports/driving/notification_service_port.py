from abc import ABC, abstractmethod
from typing import List

from domain.device import Device
from domain.notification import Notification
from domain.user import User


class NotificationServicePort(ABC):
    @abstractmethod
    def create_device(self, device: Device, user: User):
        raise NotImplementedError

    @abstractmethod
    def create_notification(self, notification: Notification) -> Notification:
        raise NotImplementedError

    @abstractmethod
    def get_devices(self, user: User) -> List[Device]:
        raise NotImplementedError

    @abstractmethod
    def send_single_notification(self, notification: Notification, token: str) -> Notification:
        raise NotImplementedError

    @abstractmethod
    def send_single_silent_notification(self, notification: Notification, token: str) -> Notification:
        raise NotImplementedError

    @abstractmethod
    def send_bulk_notification(self, notification: Notification, tokens: List[str]) -> Notification:
        raise NotImplementedError

    @abstractmethod
    def send_bulk_silent_notification(self, notification: Notification, tokens: List[str]) -> Notification:
        raise NotImplementedError
