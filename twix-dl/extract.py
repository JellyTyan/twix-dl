from .models import TweetInfo, TweetMedia


class TwitterExtractor:
    def __init__(self, tweet_url: str):
        self.tweet_url = tweet_url

    def get_tweet_info(self) -> TweetInfo:
        ...

    def _get_guest_token(self):
        ...

