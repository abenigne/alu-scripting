#!/usr/bin/python3
"""Query the Reddit API for the number of subscribers of a subreddit."""
import requests


def number_of_subscribers(subreddit):
    """Return the subscriber count of a subreddit, or 0 if it is invalid."""
    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        data = response.json().get("data")
        if not isinstance(data, dict):
            return 0
        return data.get("subscribers", 0)
    except Exception:
        return 0
