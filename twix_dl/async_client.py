from .models import TweetInfo, TweetMedia, AuthorData
import httpx
from .utils import get_random_user_agent
from typing import Dict
from typing import Any


class AsyncTwitterClient:
    def __init__(self, timeout: int = 10):
        self._auth_token = "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
        self._headers = {
            "Content-Type": "application/json",
            "User-Agent": get_random_user_agent(),
            "Authorization": f"Bearer {self._auth_token}"
            }
        self._client = httpx.AsyncClient(
            headers=self._headers,
            timeout=timeout
        )

    async def get_tweet_info(self, tweet_id: str) -> TweetInfo:
        guest_token = await self._get_guest_token()

        self._client.cookies.set("gt", guest_token, domain=".x.com")


        self._headers["X-Guest-Token"] = guest_token

        params = {
            "variables": f'{{"tweetId":"{tweet_id}","withCommunity":false,"includePromotedContent":false,"withVoice":false}}',
            'features': '{"creator_subscriptions_tweet_preview_api_enabled":true,"premium_content_api_read_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"responsive_web_grok_analyze_button_fetch_trends_enabled":false,"responsive_web_grok_analyze_post_followups_enabled":false,"responsive_web_jetfuel_frame":true,"responsive_web_grok_share_attachment_enabled":true,"articles_preview_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"responsive_web_grok_show_grok_translated_post":false,"responsive_web_grok_analysis_button_from_backend":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"payments_enabled":false,"profile_label_improvements_pcf_label_in_post_enabled":true,"rweb_tipjar_consumption_enabled":true,"verified_phone_label_enabled":false,"responsive_web_grok_image_annotation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_enhance_cards_enabled":false}',
        }

        tweet_info_url = "https://api.x.com/graphql/SAvsJgT-uo2NRaJBVX9-Hg/TweetResultByRestId"

        response = await self._client.get(tweet_info_url, headers=self._headers, params=params)

        response.raise_for_status()

        tweet_info = self.parse_tweet_info(response.json())
        return tweet_info

    async def _get_guest_token(self) -> str:
        guest_token_url = "https://api.twitter.com/1.1/guest/activate.json"

        response = await self._client.post(guest_token_url, headers=self._headers)
        response.raise_for_status()

        data = response.json()
        return data.get("guest_token")
    
    def parse_tweet_info(self, tweet_info: Dict[str, Any]) -> TweetInfo:
        tweet_data = tweet_info["data"]["tweetResult"]["result"]
        user_data = tweet_data["core"]["user_results"]["result"]
        legacy_data = tweet_data["legacy"]
        user_legacy = user_data["legacy"]
        
        # Parse author data
        author = AuthorData(
            id=user_data["id"],
            rest_id=user_data["rest_id"],
            name=user_data["core"]["name"],
            screen_name=user_data["core"]["screen_name"],
            url=f"https://x.com/{user_data['core']['screen_name']}",
            avatar_url=user_data["avatar"]["image_url"],
            profile_banner_url=user_legacy.get("profile_banner_url", ""),
            description=user_legacy.get("description", ""),
            is_blue_verified=user_data.get("is_blue_verified", False),
            favourites_count=user_legacy.get("favourites_count", 0),
            followers_count=user_legacy.get("followers_count", 0)
        )
        
        # Parse media
        media = []
        for media_data in legacy_data.get("extended_entities", {}).get("media", []):
            media.append(TweetMedia(
                type=media_data["type"],
                url=media_data["media_url_https"],
                width=media_data.get("original_info", {}).get("width"),
                height=media_data.get("original_info", {}).get("height"),
                duration=media_data.get("video_info", {}).get("duration_millis")
            ))
        
        return TweetInfo(
            tweet_id=tweet_data["rest_id"],
            url=f"https://x.com/{user_data['core']['screen_name']}/status/{tweet_data['rest_id']}",
            full_text=legacy_data["full_text"],
            author=author,
            media=media,
            favorite_count=legacy_data.get("favorite_count"),
            retweet_count=legacy_data.get("retweet_count"),
            reply_count=legacy_data.get("reply_count"),
            quote_count=legacy_data.get("quote_count"),
            lang=legacy_data.get("lang")
        )

    
    async def close(self):
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
