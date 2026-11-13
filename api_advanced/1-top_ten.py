#!/usr/bin/python3
"""
Module that queries the Reddit API and prints the titles
of the first 10 hot posts for a given subreddit.
"""
import requests


def top_ten(subreddit):
    """Prints the titles of the first 10 hot posts listed for a given subreddit."""
    if not subreddit or not isinstance(subreddit, str):
        print(None)
        return

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    
    # Custom User-Agent required by Reddit API guidelines
    headers = {'User-Agent': 'python3:alu-api_advanced:v1.0 (by /u/student)'}
    
    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        
        # If the subreddit is invalid or redirects, status code won't be 200
        if response.status_code != 200:
            print(None)
            return

        data = response.json()
        posts = data.get('data', {}).get('children', [])
        
        if not posts:
            print(None)
            return

        # Print the title of the first 10 posts
        for i in range(min(10, len(posts))):
            title = posts[i].get('data', {}).get('title')
            if title:
                print(title)

    except Exception:
        print(None)
