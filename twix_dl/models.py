from dataclasses import dataclass
from typing import Optional, List, Literal
from dataclasses import field


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