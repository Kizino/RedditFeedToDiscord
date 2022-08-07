import os
import requests
import datetime
import json
import logging
from dotenv import load_dotenv
from discord_webhook import DiscordWebhook, DiscordEmbed

load_dotenv()

# Declare variables
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK')
subreddits = ['buildapcsales'] # Can add multiple subreddits
keywords = ['RTX','SSD'] # Can add multiple keywords
exclude_sites = ['microcenter'] # Can add multiple exclusion sites

logging.basicConfig(filename='app.log',
                    filemode='a',
                    format='%(asctime)s %(name)s %(levelname)s: %(message)s',
                    datefmt='[%Y-%m-grep |%H - %H:%M:%S] ',
                    level=logging.DEBUG)

# Creating RedditPost Class
class RedditPost:  
    def __init__(self, json_object):
        base_url = "https://www.reddit.com"

        self.name = json_object['data']['name'] #name = post ID
        self.title = json_object['data']['title']
        self.created_ts = datetime.datetime.fromtimestamp(
            json_object['data']['created'])
        self.link = base_url + json_object['data']['permalink']
        self.url = json_object['data']['url']

def checkNewRedditPosts():
    data = []
    for subreddit in subreddits:
        # Sending HTTP GET request to grab newest reddit posts
        response = requests.get(f'https://www.reddit.com/r/{subreddit}/new/.json', headers={
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "User-Agent": "discord-feed-bot"})

        if response.status_code == 200:
            posts = response.json()['data']['children']

            for post in posts:
                data.append(RedditPost(post))
        else:
            pass
    
    return data

#Caching Locally to help preventing from showing duplicate post
#Open File and Load Data
def getCache():
    try:
        with open(os.path.abspath(os.path.dirname(__file__)) + '/db.json') as json_file:
            db = json.load(json_file)
    except FileNotFoundError:
        db = []

    return db

if __name__ == "__main__":
    posts = checkNewRedditPosts()
    db = getCache()

    #Append new post to DB if not already in DB
    for post in posts:
        
        if (post.name not in db) \
            and any(keyword in post.title for keyword in keywords) \
            and not any(site in post.url for site in exclude_sites):

            print(f"Found post: {post.created_ts} - {post.title} - {post.link}")
            
            #Send Webhook Event to Discord on new post
            webhook = DiscordWebhook(url=WEBHOOK_URL)
            embed = DiscordEmbed(title=post.title, description=post.created_ts.strftime('Posted on: %m/%d/%Y - %I:%M:%S') , url=post.link)
            webhook.add_embed(embed)
            status = webhook.execute().status_code

            if(status == 200):
                db.append(post.name)

    #Write to DB. Also we are only keeping lastest 100 posts
    with open(os.path.abspath(os.path.dirname(__file__)) + '/db.json', 'w') as outfile:
        json.dump(db[-100:], outfile, indent=2)

    logging.info("Script finished running.")