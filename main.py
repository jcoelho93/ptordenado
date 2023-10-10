import os
import csv
import praw
from ptordenado.post import PostParser


CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
USER_AGENT = "ptordenado/0.1.0"

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

posts = reddit.subreddit('PTOrdenado').new()
parsed_posts = []

for post in posts:
    url = post.url
    text = post.selftext
    category = post.link_flair_text

    parsed_post = PostParser(text, url, category).parse()
    print(parsed_post.parse_confidence())

    if parsed_post.parse_confidence() > 0.5:
        parsed_posts.append(parsed_post)

with open('parsed_posts.csv', mode='w') as csvfile:
    fields_names = [attr for attr in vars(parsed_posts[0])]

    writer = csv.DictWriter(csvfile, fieldnames=fields_names, delimiter=';')
    writer.writeheader()
    writer.writerows([vars(post) for post in parsed_posts])
