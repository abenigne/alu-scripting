#!/usr/bin/python3
"""Recursively count keywords in the titles of a subreddit's hot posts."""
import requests


def print_counts(counts, word_list):
    """Print the sorted keyword counts, summing duplicates in word_list."""
    multiplier = {}
    for word in word_list:
        key = word.lower()
        multiplier[key] = multiplier.get(key, 0) + 1
    totals = {}
    for word, number in counts.items():
        total = number * multiplier.get(word, 1)
        if total > 0:
            totals[word] = total
    for word, total in sorted(totals.items(), key=lambda x: (-x[1], x[0])):
        print("{}: {}".format(word, total))


def count_words(subreddit, word_list, after=None, counts=None):
    """Print the sorted count of keywords found in all hot post titles."""
    if counts is None:
        counts = {}
    if not word_list:
        return
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"limit": 100}
    if after:
        params["after"] = after
    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False)
        data = response.json().get("data")
        if not isinstance(data, dict):
            print_counts(counts, word_list)
            return
    except Exception:
        print_counts(counts, word_list)
        return
    wanted = set(word.lower() for word in word_list)
    for child in data.get("children", []):
        title = child.get("data", {}).get("title") or ""
        for word in title.lower().split():
            if word in wanted:
                counts[word] = counts.get(word, 0) + 1
    after = data.get("after")
    if after is None:
        print_counts(counts, word_list)
        return
    return count_words(subreddit, word_list, after, counts)
