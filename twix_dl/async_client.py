from .models import TweetInfo, TwitterError, TwitterOp, default_features, default_variables, ErrorExtensions, UserData
import httpx
from .utils import get_random_user_agent
import json
from .parsers import parse_tweet_info, parse_error, parse_user_info


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

    async def get_tweet_info(self, tweet_id: int) -> TweetInfo | TwitterError:
        tweet_json = await self._graphql(TwitterOp.TweetResultByRestId, variables={"tweetId": tweet_id})

        if "errors" in tweet_json:
            return parse_error(tweet_json["errors"][0])

        tweet_data = tweet_json.get("data", {}).get("tweetResult", {}).get("result")
        if not tweet_data:
            return TwitterError(
                message=f"Tweet with id {tweet_id} not found",
                code=404,
                kind="NotFound",
                name="TweetNotFound",
                source="Client",
                trace_id=None,
                extensions=ErrorExtensions(
                    name="TweetNotFound",
                    source="Client",
                    code=404,
                    kind="NotFound",
                    trace_id=None
                )
            )

        tweet_info = parse_tweet_info(tweet_json)
        return tweet_info

    async def get_user_by_username(self, screen_name: str) -> UserData | TwitterError:
        user_json = await self._graphql(TwitterOp.UserByScreenName, variables={"screen_name": screen_name})
        
        if "errors" in user_json:
            return parse_error(user_json["errors"][0])
            
        user_data = user_json.get("data", {}).get("user", {}).get("result")
        if not user_data:
            return TwitterError(
                message=f"User {screen_name} not found",
                code=404,
                kind="NotFound",
                name="UserNotFound",
                source="Client",
                trace_id=None,
                extensions=ErrorExtensions(
                    name="UserNotFound",
                    source="Client",
                    code=404,
                    kind="NotFound",
                    trace_id=None
                )
            )
            
        return parse_user_info(user_json)

    async def _get_guest_token(self) -> str:
        guest_token_url = "https://api.twitter.com/1.1/guest/activate.json"

        response = await self._client.post(guest_token_url, headers=self._headers)
        response.raise_for_status()

        data = response.json()
        return data.get("guest_token")

    async def _graphql(self, op: TwitterOp, **variables):
        user_vars = variables.get("variables", {})
        user_features = variables.get("features", {})

        final_variables = {**default_variables, **user_vars}
        final_features = {**default_features, **user_features}

        params = {
            "variables": json.dumps(final_variables, separators=(",", ":")),
            "features": json.dumps(final_features, separators=(",", ":")),
        }

        guest_token = await self._get_guest_token()
        self._client.cookies.set("gt", guest_token, domain=".x.com")
        self._headers["X-Guest-Token"] = guest_token
        url = f"https://api.x.com/graphql/{op.value.operation_id}/{op.value.name}"
        response = await self._client.get(url, params=params, headers=self._headers)
        response.raise_for_status()
        
        if not response.content:
            raise ValueError("Empty response from Twitter API")
            
        return response.json()

    async def close(self):
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
