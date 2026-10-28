#!/usr/bin/python3
"""Recursively collect the titles of all hot posts of a subreddit."""
import requests

USER_AGENT = "linux:alu.api_advanced:v1.0.0 (by /u/alu_student)"


def recurse(subreddit, hot_list=None, after=None):
    """Return a list of all hot post titles, or None if nothing is found."""
    if hot_list is None:
        hot_list = []
    if not isinstance(subreddit, str):
        return None
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    params = {"limit": 100}
    if after:
        params["after"] = after
    response = requests.get(url, headers={"User-Agent": USER_AGENT},
                            params=params, allow_redirects=False)
    if response.status_code != 200:
        return hot_list if hot_list else None
    try:
        data = response.json().get("data", {})
    except ValueError:
        return hot_list if hot_list else None
    for child in data.get("children", []):
        hot_list.append(child.get("data", {}).get("title"))
    after = data.get("after")
    if after is None:
        return hot_list if hot_list else None
    return recurse(subreddit, hot_list, after)
