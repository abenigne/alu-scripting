#!/usr/bin/python3
"""Query the Reddit API for the number of subscribers of a subreddit."""
import requests

USER_AGENT = "linux:alu.api_advanced:v1.0.0 (by /u/alu_student)"


def number_of_subscribers(subreddit):
    """Return the subscriber count of a subreddit, or 0 if it is invalid."""
    if not isinstance(subreddit, str):
        return 0
    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    response = requests.get(url, headers={"User-Agent": USER_AGENT},
                            allow_redirects=False)
    if response.status_code != 200:
        return 0
    try:
        data = response.json().get("data", {})
    except ValueError:
        return 0
    return data.get("subscribers", 0)
