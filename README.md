# TwiX-dl

<img src="https://raw.githubusercontent.com/JellyTyan/twix-dl/main/.github/assets/twix.png" height="300px"/>

`twix-dl` is a Python library (and future CLI tool) for extracting tweet metadata and downloading all media attachments (photos, videos, GIFs) from a Twitter/X post.


## 📦 Installation

(For now, install from source)

```bash
git clone https://github.com/JellyTyan/twix-dl.git
cd twix-dl
pip install -e .
````

*(PyPI package coming soon: `pip install twix-dl`)*

---

## 📚 Data Structures

```python
@dataclass
class TweetMedia:
    type: str             # "photo", "video", "gif"
    url: str              # direct media URL
    width: Optional[int]
    height: Optional[int]
    duration: Optional[int]  # for videos
    size: Optional[int]      # optional file size

@dataclass
class TweetInfo:
    tweet_id: str
    url: str
    text: Optional[str]
    author: Optional[str]
    author_url: Optional[str]
    author_avatar: Optional[str]
    media: List[TweetMedia]
```