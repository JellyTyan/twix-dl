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
    name: str
    screen_name: str
    url: str
    avatar_url: str
    description: str
    is_blue_verified: bool
    followers_count: int
    # ... more fields

@dataclass
class TweetMedia:
    type: str             # "photo", "video", "gif"
    url: str              # direct media URL
    width: Optional[int]
    height: Optional[int]
    duration: Optional[int]  # for videos

@dataclass
class TweetInfo:
    tweet_id: str
    url: str
    full_text: Optional[str]
    author: AuthorData
    media: List[TweetMedia]
    favorite_count: Optional[int]
    retweet_count: Optional[int]
    reply_count: Optional[int]
    # ... more fields
```