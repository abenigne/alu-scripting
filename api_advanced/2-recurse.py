#!/usr/bin/python3
"""Recursively collect the titles of all hot posts of a subreddit."""
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


def recurse(subreddit, hot_list=None, after=None):
    """Return a list of all hot post titles, or None if nothing is found."""
    if hot_list is None:
        hot_list = []
    if not isinstance(subreddit, str):
        return None
    params = {"limit": 100}
    if after:
        params["after"] = after
    result = fetch(subreddit, "hot", params)
    if not result:
        return hot_list if hot_list else None
    data = result.get("data", {})
    for child in data.get("children", []):
        hot_list.append(child.get("data", {}).get("title"))
    after = data.get("after")
    if after is None:
        return hot_list if hot_list else None
    return recurse(subreddit, hot_list, after)
