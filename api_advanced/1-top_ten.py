#!/usr/bin/python3
"""
Module to query the Reddit API and print the titles
of the first 10 hot posts for a given subreddit.
"""
import requests


def top_ten(subreddit):
    """Prints the titles of the first 10 hot posts for a subreddit."""
    if subreddit is None or not isinstance(subreddit, str):
        print(None)
        return

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {'User-Agent': 'python:alu-api_advanced:v1.0 (by /u/student)'}
    parameters = {'limit': 10}

    response = requests.get(url, headers=headers,
                            params=parameters,
                            allow_redirects=False)

    if response.status_code != 200:
        print(None)
        return

    try:
        data = response.json().get('data', {})
        children = data.get('children', [])
        if not children:
            print(None)
            return
        for child in children:
            print(child.get('data', {}).get('title'))
    except Exception:
        print(None)

