from abc import ABC, abstractmethod

from domain.apple_info import AppleInfo


class AppleRepositoryPort(ABC):
    @abstractmethod
    def validate_token(self, auth_code: str) -> AppleInfo | None:
        pass
