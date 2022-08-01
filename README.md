# RedditFeedToDiscord
- This script is used to monitor reddit posts in specified subreddits that contain specified keywords.
- If a post is found that satisfied above conditions, the script will send a webhook message to discord to post in a specified discord channel

**Example:**
```
subreddits = ['buildapcsales']
keywords = ['RTX','SSD']
exclude_sites = ['microcenter']
```
The script will monitor [buildapcsales](https://www.reddit.com/r/buildapcsales) subreddit to find any posts that contain "RTX" or "SSD" keywords and not
have link to microcenter website
