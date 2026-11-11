#!/usr/bin/python3
"""
Recursive function to query Reddit API and return a list
containing the titles of all hot articles for a given subreddit.
"""

import requests


def recurse(subreddit, hot_list=[], after=""):
    """Queries the Reddit API recursively and returns a list of hot post titles."""
    headers = {'User-Agent': 'python3:alu-api-advanced:v1.0 (by /u/student)'}
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    params = {'after': after}

    response = requests.get(url, headers=headers, params=params,
                            allow_redirects=False)

    if response.status_code != 200:
        return None

    try:
        data = response.json().get('data')
        after = data.get('after')
        children = data.get('children')

        for child in children:
            hot_list.append(child.get('data').get('title'))

        if after is not None:
            return recurse(subreddit, hot_list, after)
        return hot_list
    except Exception:
        return None
