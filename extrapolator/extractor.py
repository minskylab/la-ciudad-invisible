import os
import time

from dataclasses import asdict
from arango.database import StandardDatabase
from extrapolator.post import CleanPost
from typing import Tuple
from instaloader.instaloader import Instaloader, Post
from datetime import datetime, timedelta
from random import random
from minio.api import Minio
from .relevance import relevance
from instaloader import Hashtag
from itertools import dropwhile, takewhile
from threading import Thread
from pathlib import Path
from os import path
from queue import Queue


def extractor_loader(store: Minio, db: StandardDatabase, query: str, delay_hours: int, period_seconds: int) -> Tuple[Thread, Queue]:
    loader = Instaloader()
    user, password = os.getenv("IG_USERNAME"), os.getenv("IG_PASSWORD")

    try:
        loader.load_session_from_file(user, "session")
    except:
        loader.login(user, password)
        loader.save_session_to_file("session")

    # create data dir
    data_dir = os.getenv("DATA_DIR", "data/")
    Path(data_dir).mkdir(exist_ok=True)

    # q = Queue[CleanPost]()
    q = Queue()

    t = Thread(target=fetch_loop, args=(
        store, db, loader, query, delay_hours, period_seconds, q))

    return (t, q)


def fetch_loop(store: Minio, db: StandardDatabase, loader: Instaloader, query: str, delay_hours: int, period_seconds: int, q: Queue):
    data_dir = os.getenv("DATA_DIR", "data/")

    while True:
        posts = Hashtag.from_name(loader.context, query).get_posts()

        since = datetime.now() - timedelta(hours=delay_hours, seconds=period_seconds)
        until = since + timedelta(seconds=period_seconds)

        print(since, "-", until)

        for post in takewhile(lambda p: p.date_local > since, dropwhile(lambda p: p.date_local > until, posts)):
            post = process_post(loader, db, post, store, data_dir)
            q.put(post, False)

        time.sleep(period_seconds + int(random()*5))


def process_post(loader: Instaloader, db: StandardDatabase, post: Post, store: Minio, data_dir: str) -> CleanPost:
    likes = post.likes
    comments = post.comments
    date = post.date_local
    _id = post.shortcode

    rel = relevance(likes, comments)

    print(f"-- [{_id}]: L: {likes}, C: {comments}, D: {date}, R: {rel}")

    filepath = path.join(data_dir, post.shortcode)
    loader.download_pic(filepath, post.url, post.date)

    bucket = os.getenv("S3_BUCKET", "")
    endpoint = os.getenv("S3_ENDPOINT", "")
    prefix = os.getenv("S3_DATA_DIR_NAME", "data")

    destination = post.shortcode + ".jpg"

    try:
        etag, n_id = store.fput_object(
            bucket, destination, filepath, content_type="image/jpg")
        print(etag, n_id)
    except:
        print("Error at save object")
        return

    link = f"https://{bucket}.{endpoint}/{prefix}/{destination}"

    p = CleanPost(
        id=post.shortcode,
        date=post.date_local,
        likes=post.likes,
        comments=post.comments,
        hashtags=post.caption_hashtags,
        mentions=post.caption_mentions,
        relevance=rel,
        imageURI=link,
    )

    coll_name = "Posts"

    try:
        db.create_collection(coll_name)
    except:
        print("error at execute create collection")

    posts = db.collection(coll_name)

    posts.insert(asdict(p))

    if path.exists(filepath):
        os.remove(filepath)

    return p
