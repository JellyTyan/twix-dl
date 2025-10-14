from dataclasses import dataclass
from typing import Optional, List, Literal, Dict, Any
from dataclasses import field
from enum import Enum


@dataclass(slots=True)
class AuthorData:
    """Metadata about the tweet author."""
    id: str                  # Twitter internal numeric ID
    rest_id: str             # String version of ID (redundant but present in API)
    name: str                # Display name (e.g. "Elon Musk")
    screen_name: str         # @handle
    url: str                 # Link to profile
    avatar_url: str          # Profile picture
    profile_banner_url: str  # Header banner
    description: str         # Bio text

    is_blue_verified: bool   # X Blue / Verified status

    favourites_count: int    # How many likes author has given
    followers_count: int     # How many followers they have


@dataclass(slots=True)
class TweetMedia:
    """Single media item attached to a tweet."""
    type: Literal["photo", "video", "gif"]
    url: str

    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None   # For videos / GIFs
    size: Optional[int] = None       # Approx file size (bytes, optional)


@dataclass(slots=True)
class TweetInfo:
    """Parsed tweet data."""
    tweet_id: str
    url: str
    full_text: Optional[str]

    author: AuthorData
    media: List[TweetMedia] = field(default_factory=list)

    favorite_count: Optional[int] = None
    retweet_count: Optional[int] = None
    reply_count: Optional[int] = None
    quote_count: Optional[int] = None

    lang: Optional[str] = None


@dataclass(slots=True)
class ErrorExtensions:
    name: str
    source: str
    code: int
    kind: str
    trace_id: Optional[str] = None


@dataclass(slots=True)
class TwitterError:
    """Twitter response error"""
    message: str
    code: int
    kind: str
    name: str
    source: str
    trace_id: Optional[str]
    extensions: ErrorExtensions


@dataclass(frozen=True)
class GraphQLOperation:
    variables_schema: Dict[str, Any]
    operation_id: str
    name: str

    def build_payload(self, **kwargs) -> Dict[str, Any]:
        missing_vars = [key for key in self.variables_schema if key not in kwargs]
        if missing_vars:
            raise ValueError(f"Missing required variables: {', '.join(missing_vars)}")
        return {
            "queryId": self.operation_id,
            "variables": kwargs
        }


class TwitterOp(Enum):
    TweetResultByRestId = GraphQLOperation({'tweetId': int}, 'WvlrBJ2bz8AuwoszWyie8A', 'TweetResultByRestId')

# Core query variables
_CORE_VARS = {
    'count': 1000,
    'withSafetyModeUserFields': True,
    'includePromotedContent': True,
    'withQuickPromoteEligibilityTweetFields': True,
    'withVoice': True,
    'withV2Timeline': True,
    'withDownvotePerspective': False,
    'withBirdwatchNotes': True,
    'withCommunity': True,
    'withSuperFollowsUserFields': True,
    'withReactionsMetadata': False,
    'withReactionsPerspective': False,
    'withSuperFollowsTweetFields': True,
    'isMetatagsQuery': False,
    'withReplays': True,
    'withClientEventToken': False,
    'withAttachments': True,
    'withConversationQueryHighlights': True,
    'withMessageQueryHighlights': True,
    'withMessages': True,
}

# Core features
_CORE_FEATURES = {
    'c9s_tweet_anatomy_moderator_badge_enabled': True,
    'responsive_web_home_pinned_timelines_enabled': True,
    'blue_business_profile_image_shape_enabled': True,
    'interactive_text_enabled': True,
    'graphql_is_translatable_rweb_tweet_is_translatable_enabled': True,
    'graphql_timeline_v2_bookmark_timeline': True,
    'responsive_web_graphql_exclude_directive_enabled': True,
    'responsive_web_edit_tweet_api_enabled': True,
    'responsive_web_twitter_blue_verified_badge_is_enabled': True,
}

# Content features
_CONTENT_FEATURES = {
    'articles_preview_enabled': False,
    'longform_notetweets_consumption_enabled': True,
    'longform_notetweets_inline_media_enabled': True,
    'longform_notetweets_rich_text_read_enabled': True,
    'longform_notetweets_richtext_consumption_enabled': True,
    'responsive_web_media_download_video_enabled': False,
    'responsive_web_twitter_article_data_v2_enabled': True,
    'responsive_web_twitter_article_tweet_consumption_enabled': False,
}

# Disabled features
_DISABLED_FEATURES = {
    'payments_enabled': False,
    'premium_content_api_read_enabled': False,
    'responsive_web_enhance_cards_enabled': False,
    'responsive_web_text_conversations_enabled': False,
    'responsive_web_profile_redirect_enabled': False,
    'responsive_web_jetfuel_frame': False,
    'rweb_tipjar_consumption_enabled': False,
    'tweet_awards_web_tipping_enabled': False,
    'verified_phone_label_enabled': False,
    'creator_subscriptions_quote_tweet_preview_enabled': False,
    'communities_web_enable_tweet_community_results_fetch': False,
    'profile_label_improvements_pcf_label_in_post_enabled': False,
    'responsive_web_graphql_skip_user_profile_image_extensions_enabled': False,
}

# Grok features (all disabled)
_GROK_FEATURES = {
    'responsive_web_grok_show_grok_translated_post': False,
    'responsive_web_grok_share_attachment_enabled': False,
    'responsive_web_grok_community_note_auto_translation_is_enabled': False,
    'responsive_web_grok_analyze_post_followups_enabled': False,
    'responsive_web_grok_image_annotation_enabled': False,
    'responsive_web_grok_imagine_annotation_enabled': False,
    'responsive_web_grok_analysis_button_from_backend': False,
    'responsive_web_grok_analyze_button_fetch_trends_enabled': False,
}

# Other enabled features
_OTHER_FEATURES = {
    'creator_subscriptions_tweet_preview_api_enabled': True,
    'freedom_of_speech_not_reach_fetch_enabled': True,
    'hidden_profile_likes_enabled': True,
    'highlights_tweets_tab_ui_enabled': True,
    'profile_foundations_tweet_stats_enabled': True,
    'profile_foundations_tweet_stats_tweet_frequency': True,
    'responsive_web_birdwatch_note_limit_enabled': True,
    'responsive_web_graphql_timeline_navigation_enabled': True,
    'rweb_lists_timeline_redesign_enabled': True,
    'spaces_2022_h2_clipping': True,
    'spaces_2022_h2_spaces_communities': True,
    'standardized_nudges_misinfo': True,
    'subscriptions_verification_info_verified_since_enabled': True,
    'tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled': True,
    'tweetypie_unmention_optimization_enabled': True,
    'vibe_api_enabled': True,
    'view_counts_everywhere_api_enabled': True,
}

default_variables = _CORE_VARS
default_features = {**_CORE_FEATURES, **_CONTENT_FEATURES, **_DISABLED_FEATURES, **_GROK_FEATURES, **_OTHER_FEATURES}
