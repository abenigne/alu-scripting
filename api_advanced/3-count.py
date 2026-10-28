#!/usr/bin/python3
"""Recursively count keywords in the titles of a subreddit's hot posts."""
import requests

USER_AGENT = "linux:alu.api_advanced:v1.0.0 (by /u/alu_student)"


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
    if not isinstance(subreddit, str) or not word_list:
        return
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    params = {"limit": 100}
    if after:
        params["after"] = after
    response = requests.get(url, headers={"User-Agent": USER_AGENT},
                            params=params, allow_redirects=False)
    if response.status_code != 200:
        print_counts(counts, word_list)
        return
    try:
        data = response.json().get("data", {})
    except ValueError:
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
