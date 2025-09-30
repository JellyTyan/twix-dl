from dataclasses import dataclass
from typing import Optional, List
from dataclasses import field


@dataclass
class TweetMedia:
    type: str
    url: str
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None
    size: Optional[int] = None

@dataclass
class TweetInfo:
    tweet_id: str
    url: str
    text: Optional[str]
    author: Optional[str] = None
    author_url: Optional[str] = None
    author_avatar: Optional[str] = None
    media: List[TweetMedia] = field(default_factory=list)
