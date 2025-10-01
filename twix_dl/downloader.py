from typing import List
from .models import TweetInfo, TweetMedia


class TwitterDownloader:
    def __init__(self, tweet_info: TweetInfo):
        self.tweet_info = tweet_info

    def download_media(self) -> List[str]:
        ...

    def _download_file(self, media: TweetMedia, output_dir: str) -> str:
        ...