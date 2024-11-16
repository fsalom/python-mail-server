from typing import Dict, Any

from domain.google_info import GoogleInfo


class GoogleInfoMapper:
    @staticmethod
    def from_json_to_entity(google_info_response: Dict[str, Any]) -> GoogleInfo:
        return GoogleInfo(
            email=google_info_response.get("email", ''),
            family_name=google_info_response.get("family_name", ''),
            given_name=google_info_response.get("given_name", ''),
        )
