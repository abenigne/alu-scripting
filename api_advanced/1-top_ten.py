#!/usr/bin/python3
"""Print the titles of the first 10 hot posts of a subreddit."""
import requests


def top_ten(subreddit):
    """Print the first 10 hot post titles, or None if subreddit is invalid."""
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers,
                                params={"limit": 10}, allow_redirects=False)
        data = response.json().get("data")
        if not isinstance(data, dict):
            print(None)
            return
        for child in data.get("children", [])[:10]:
            print(child.get("data", {}).get("title"))
    except Exception:
        print(None)
