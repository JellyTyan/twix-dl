import asyncio
from typing import Any, Dict
from .models import TweetInfo
from .async_client import AsyncTwitterClient

class TwitterClient:
    """
    Синхронная обертка над асинхронным клиентом.
    Предоставляет пользователю привычный синхронный API.
    """
    def __init__(self, auth_token: str, timeout: int = 10):
        self._async_client = AsyncTwitterClient()
        
        try:
            self._loop = asyncio.get_running_loop()
        except RuntimeError:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)

    def _run_async(self, coro):
        """Хелпер для запуска асинхронной функции в event loop."""
        return self._loop.run_until_complete(coro)

    def get_tweet(self, tweet_id: str) -> TweetInfo:
        """
        Синхронно получает данные одного твита.
        """
        print("Выполняется синхронный вызов (через async)...")
        return self._run_async(self._async_client.get_tweet_info(tweet_id))
    
    def close(self):
        """Закрывает сессию."""
        self._run_async(self._async_client.close())
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()