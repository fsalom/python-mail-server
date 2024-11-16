from typing import Dict, Any

from domain.apple_info import AppleInfo


class AppleInfoMapper:
    @staticmethod
    def from_json_to_entity(apple_info_response: Dict[str, Any]) -> AppleInfo:
        return AppleInfo(
            email=apple_info_response.get('email'),
            sub=apple_info_response.get('sub')
        )
