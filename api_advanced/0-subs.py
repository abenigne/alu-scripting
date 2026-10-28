#!/usr/bin/python3
"""Query the Reddit API for the number of subscribers of a subreddit."""
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


def number_of_subscribers(subreddit):
    """Return the subscriber count of a subreddit, or 0 if it is invalid."""
    if not isinstance(subreddit, str):
        return 0
    result = fetch(subreddit, "about")
    if not result:
        return 0
    return result.get("data", {}).get("subscribers", 0)
