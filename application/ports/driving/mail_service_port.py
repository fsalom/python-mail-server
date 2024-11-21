from abc import ABC, abstractmethod

from domain.mail import Mail
from domain.ticket import Ticket


class MailServicePort(ABC):
    @abstractmethod
    def process(self):
        pass

    @abstractmethod
    def test(self):
        pass
