from abc import ABC, abstractmethod
from typing import List

from domain.device import Device
from domain.notification import Notification
from domain.user import User


class NotificationDBRepositoryPort(ABC):
    @abstractmethod
    def create_device(self, device: Device, user: User):
        raise NotImplementedError

    @abstractmethod
    def get_devices(self, user: User) -> List[Device]:
        raise NotImplementedError

    @abstractmethod
    def create_notification(self, notification: Notification) -> Notification:
        raise NotImplementedError

    @abstractmethod
    def add_notification_to_user(self, notification: Notification, user: User):
        raise NotImplementedError

    @abstractmethod
    def remove_device(self, device_id: str):
        raise NotImplementedError
