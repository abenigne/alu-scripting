#!/usr/bin/python3
"""Print the titles of the first 10 hot posts of a subreddit."""
import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/120.0 Safari/537.36"}
URLS = ["https://api.reddit.com/r/{}/{}",
        "https://www.reddit.com/r/{}/{}.json",
        "https://old.reddit.com/r/{}/{}.json"]


def fetch(subreddit, page, params=None):
    """Return the JSON of a subreddit page, or None on any failure."""
    for template in URLS:
        try:
            res = requests.get(template.format(subreddit, page),
                               headers=HEADERS, params=params,
                               allow_redirects=False, timeout=10)
            if res.status_code == 200:
                return res.json()
        except (requests.RequestException, ValueError):
            continue
    return None


def top_ten(subreddit):
    """Print the first 10 hot post titles, or None if subreddit is invalid."""
    if not isinstance(subreddit, str):
        print(None)
        return
    result = fetch(subreddit, "hot", {"limit": 10})
    if not result:
        print(None)
        return
    for child in result.get("data", {}).get("children", [])[:10]:
        print(child.get("data", {}).get("title"))
