#!/usr/bin/python3
"""Recursively count keywords in the titles of a subreddit's hot posts."""
import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/120.0 Safari/537.36"}
URLS = ["https://api.reddit.com/r/{}/{}",
        "https://www.reddit.com/r/{}/{}.json",
        "https://old.reddit.com/r/{}/{}.json"]


def fetch(subreddit, page, params=None):
    """Return the JSON of a subreddit page, or None on any failure."""
    for template in URLS:
        try:
            res = requests.get(template.format(subreddit, page),
                               headers=HEADERS, params=params,
                               allow_redirects=False, timeout=10)
            if res.status_code == 200:
                return res.json()
        except (requests.RequestException, ValueError):
            continue
    return None


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
    params = {"limit": 100}
    if after:
        params["after"] = after
    result = fetch(subreddit, "hot", params)
    if not result:
        print_counts(counts, word_list)
        return
    data = result.get("data", {})
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
