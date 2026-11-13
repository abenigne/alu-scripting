#!/usr/bin/python3
"""
Module to query the Reddit API and print the titles
of the first 10 hot posts for a given subreddit.
"""
import requests


def top_ten(subreddit):
    """Prints the titles of the first 10 hot posts for a subreddit."""
    if not subreddit or not isinstance(subreddit, str):
        print(None)
        return

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    
    # Reddit officially requires this custom descriptive User-Agent format
    headers = {'User-Agent': 'linux:alu.api.advanced:v1.0 (by /u/student)'}

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        
        if response.status_code != 200:
            print(None)
            return

        data = response.json()
        posts = data.get('data', {}).get('children', [])
        if not posts:
            print(None)
            return

        for i in range(min(10, len(posts))):
            title = posts[i].get('data', {}).get('title')
            if title:
                print(title)
    except Exception:
        print(None)
