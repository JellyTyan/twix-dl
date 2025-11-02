from ..models import UserData
from typing import Dict, Any

def parse_user_info(user_json: Dict[str, Any]) -> UserData:
    user_data = user_json["data"]["user"]["result"]
    user_legacy = user_data["legacy"]
    
    return UserData(
        id=user_data["id"],
        rest_id=user_data["rest_id"],
        name=user_data["core"]["name"],
        screen_name=user_data["core"]["screen_name"],
        description=user_legacy.get("description", ""),
        location=user_data.get("location", {}).get("location"),
        avatar_url=user_data["avatar"]["image_url"],
        profile_banner_url=user_legacy.get("profile_banner_url", ""),
        profile_url=user_legacy.get("entities", {}).get("url", {}).get("urls", [{}])[0].get("expanded_url"),
        is_blue_verified=user_data.get("is_blue_verified", False),
        is_verified=user_data.get("verification", {}).get("verified", False),
        is_protected=user_data.get("privacy", {}).get("protected", False),
        followers_count=user_legacy.get("followers_count", 0),
        following_count=user_legacy.get("friends_count", 0),
        favourites_count=user_legacy.get("favourites_count", 0),
        statuses_count=user_legacy.get("statuses_count", 0),
        created_at=user_data["core"]["created_at"]
    )