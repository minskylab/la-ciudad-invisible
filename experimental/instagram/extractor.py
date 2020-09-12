from datetime import datetime, timedelta
import random

from consume import relevance
import os
from instaloader import Instaloader, Hashtag
from dotenv import load_dotenv
from itertools import dropwhile, takewhile
import time


load_dotenv(dotenv_path="credentials.env", verbose=True)

loader = Instaloader()
user, password = os.getenv("IG_USERNAME"), os.getenv("IG_PASSWORD")

try:
    loader.load_session_from_file(user, "session")
except:
    loader.login(user, password)
    loader.save_session_to_file("session")


query = "cusco"
target = "data"

past_hours = 1
window_seconds = 120

while True:
    posts = Hashtag.from_name(loader.context, query).get_posts()

    since = datetime.now() - timedelta(hours=past_hours, seconds=window_seconds)
    until = since + timedelta(seconds=window_seconds)

    print(since, " - ", until)
    # filtered_posts = filter(lambda p: since <= p.date <= until, posts)
    # for post in filtered_posts:
    for post in takewhile(lambda p: p.date_local > since, dropwhile(lambda p: p.date_local > until, posts)):
        likes = post.likes
        comments = post.comments
        date = post.date_local

        filepath = "data/"+post.shortcode

        rel = relevance(likes, comments)
        print(f"-- [{post.shortcode}]", likes, comments, date, rel)
        loader.download_pic(filepath, post.url, date)
        print("")

    time.sleep(window_seconds)
