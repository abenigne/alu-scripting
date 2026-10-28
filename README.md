# alu-scripting

## api_advanced

Python scripts that query the Reddit API:

- 0-subs.py: number_of_subscribers(subreddit) returns the subscriber count (0 if invalid)
- 1-top_ten.py: top_ten(subreddit) prints the titles of the first 10 hot posts (None if invalid)
- 2-recurse.py: recurse(subreddit) recursively returns the titles of all hot posts (None if invalid)
- 3-count.py: count_words(subreddit, word_list) recursively counts keywords in hot post titles and prints them sorted

All scripts use the requests module, a custom User-Agent and do not follow redirects.
