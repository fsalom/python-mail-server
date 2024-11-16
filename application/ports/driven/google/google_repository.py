from abc import ABC, abstractmethod

from domain.google_info import GoogleInfo


class GoogleRepositoryPort(ABC):
    @abstractmethod
    def validate_token(self, id_token: str) -> GoogleInfo | None:
        pass
