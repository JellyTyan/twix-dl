import asyncio
from typing import Any, Dict
from .models import TweetInfo, TwitterError, UserData
from .async_client import AsyncTwitterClient

class TwitterClient:
    """
    Synchronous wrapper over asynchronous client.
    Provides user with familiar synchronous API.    """
    def __init__(self, timeout: int = 10):
        self._async_client = AsyncTwitterClient()
        
        try:
            self._loop = asyncio.get_running_loop()
        except RuntimeError:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)

    def _run_async(self, coro):
        """Helper for running asynchronous function"""
        return self._loop.run_until_complete(coro)

    def get_tweet_info(self, tweet_id: int) -> TweetInfo | TwitterError:
        """
        Synchronously retrieves data from a single tweet.
        """
        return self._run_async(self._async_client.get_tweet_info(tweet_id))
    
    def get_user_by_username(self, screen_name: str) -> UserData | TwitterError:
        """
        Synchronously retrieves user data by screen name.
        """
        return self._run_async(self._async_client.get_user_by_username(screen_name))
    
    def close(self):
        """Closes the session."""
        self._run_async(self._async_client.close())
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()