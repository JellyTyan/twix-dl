# TwiX-dl

[![PyPI version](https://badge.fury.io/py/twix-dl.svg)](https://badge.fury.io/py/twix-dl)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

<img src="https://raw.githubusercontent.com/JellyTyan/twix-dl/main/.github/assets/twix.png" height="300px"/>

`twix-dl` is a Python library (and future CLI tool) for extracting tweet metadata and downloading all media attachments (photos, videos, GIFs) from a Twitter/X post.

## 📦 Installation

```bash
pip install twix-dl
```

**Or install from source:**

```bash
git clone https://github.com/JellyTyan/twix-dl.git
cd twix-dl
pip install -e .
```



---

## 📚 Data Structures

```python
@dataclass
class AuthorData:
    id: str
    rest_id: str
    name: str
    screen_name: str
    url: str
    avatar_url: str
    profile_banner_url: str
    description: str
    is_blue_verified: bool
    favourites_count: int
    followers_count: int

@dataclass
class TweetMedia:
    type: Literal["photo", "video", "gif"]
    url: str
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None  # for videos/GIFs
    size: Optional[int] = None      # file size in bytes

@dataclass
class TweetInfo:
    tweet_id: str
    url: str
    full_text: Optional[str]
    author: AuthorData
    media: List[TweetMedia]
    favorite_count: Optional[int] = None
    retweet_count: Optional[int] = None
    reply_count: Optional[int] = None
    quote_count: Optional[int] = None
    lang: Optional[str] = None

@dataclass
class ErrorExtensions:
    name: str
    source: str
    code: int
    kind: str
    trace_id: Optional[str] = None

@dataclass
class TwitterError:
    """Twitter API error response"""
    message: str
    code: int
    kind: str
    name: str
    source: str
    trace_id: Optional[str]
    extensions: ErrorExtensions

@dataclass(frozen=True)
class GraphQLOperation:
    """GraphQL operation definition for Twitter API"""
    variables_schema: Dict[str, Any]
    operation_id: str
    name: str
```
