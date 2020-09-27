from cropper import crop_image
import os
import re
from .post import CleanPost
from os import path
from extrapolator.relevance import relevance
from queue import Queue
from threading import Thread
import time
from typing import List, Tuple
from minio.api import Minio
import requests
from datetime import datetime, timedelta, timezone
from pathlib import Path
from itertools import dropwhile, takewhile
from random import random
import shutil


def load_fql_query(filepath: str = "scraper.aql") -> str:
    scraper_descr = open(filepath, "r")
    return scraper_descr.read()


def extractor(store: Minio, query: str, delay_seconds: int, period_seconds: int) -> Tuple[Thread, Queue]:
    user, password = os.getenv("IG_USERNAME"), os.getenv("IG_PASSWORD")

    data_dir = os.getenv("DATA_DIR", "data/")
    Path(data_dir).mkdir(exist_ok=True)

    q = Queue()

    t = Thread(target=fetch_loop, args=(
        store, user, password, query, delay_seconds, period_seconds, q))

    return (t, q)


def fetch_loop(store: Minio, username: str, password: str, query: str, delay_seconds: int, period_seconds: int, q: Queue):
    data_dir = os.getenv("DATA_DIR", "data/")

    worker_endpoint = os.getenv(
        "FERRET_WORKER_ENDPOINT",
        "http://localhost:8080",
    )

    while True:
        posts = extract_posts(worker_endpoint, username, password, query)

        if os.getenv("PROD", False):
            now = datetime.now() - timedelta(hours=5)
        else:
            now = datetime.now()

        since = now - timedelta(seconds=delay_seconds+period_seconds)
        until = since + timedelta(seconds=period_seconds)

        print(since, "-", until, f"[{len(posts)}]")

        for post in takewhile(lambda p: datetime.strptime(p.date, '%Y-%m-%dT%H:%M:%S') > since, dropwhile(lambda p: datetime.strptime(p.date, '%Y-%m-%dT%H:%M:%S') > until, posts)):
            post = process_post(store, post, data_dir)
            q.put(post, False)

        time.sleep(period_seconds + int(random()*5))


def download_pic(filepath: str, image_url: str):
    if image_url == "" or image_url == None:
        return

    response = requests.get(image_url, stream=True)
    with open(filepath, 'wb+') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


def process_post(store: Minio, post: CleanPost, data_dir: str) -> CleanPost:
    likes = post.likes
    comments = post.comments
    date = post.date
    _id = post.id

    rel = relevance(likes, comments)

    print(f"~ [{_id}]: L: {likes}, C: {comments}, D: {date}, R: {rel}")

    filepath = path.join(data_dir, post.id)

    bucket = os.getenv("S3_BUCKET", "")
    endpoint = os.getenv("S3_ENDPOINT", "")
    folder_name = os.getenv("S3_DATA_DIR_NAME", "laciudadinvisible")

    destination = folder_name + "/" + post.id + ".jpg"

    full_filepath = filepath + ".jpg"

    download_pic(full_filepath, post.image_uri)

    post_processed_img = crop_image(full_filepath)

    store.fput_object(bucket,
                      destination,
                      post_processed_img,
                      content_type="image/jpg",
                      metadata={"x-amz-acl": "public-read"})

    link = f"https://{bucket}.{endpoint}/{destination}"

    full_comments = post.comments_content

    p = CleanPost(
        id=post.id,
        date=post.date,
        likes=post.likes,
        comments=post.comments,
        hashtags=post.hashtags,
        mentions=post.mentions,
        relevance=rel,
        image_uri=link,
        description=post.description,
        comments_content=full_comments,
    )

    return p


# 2m28s, 1m54s, 1m49s
def extract_posts(worker_endpoint: str, username: str, password: str, query: str, retry: int = 0) -> List[CleanPost]:
    start = time.time()
    q = load_fql_query()

    print("scraping start")

    res = requests.post(worker_endpoint, json={
        "text": q,
        "params": {
            "query": query,
            "username": username,
            "password": password
        }
    })

    data = res.json()

    if len(data) < 2:  # error
        err = data["error"] if "error" in data else data
        print(err)
        if "error" in data and retry < 5:
            print("scraping retrying")
            time.sleep(int(random()*3))
            return extract_posts(worker_endpoint, username, password, query, retry + 1)
        print("scraping abort")
        return []

    posts: List[CleanPost] = []

    for post in data:
        if "id" not in post:
            continue

        if "img" not in post:
            continue

        post_id = post["id"]
        img = post["img"]
        items = post["raw_items"]
        date = post["date"]
        likes = post["likes"]

        if img is None:  # no image, probably it's a video
            continue

        d = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
        local_date = d-timedelta(hours=5)

        final_date = local_date.isoformat()

        f_comment = items[0] if len(items) > 0 else ""

        hashtags = re.findall(r"#\w+", f_comment)
        mentions = re.findall(r"@\w+", f_comment)

        total_comments = len(items)-1 if len(items) > 0 else 0

        comments = items[1:] if len(items) > 1 else []

        clean_p = CleanPost(
            id=post_id,
            hashtags=hashtags,
            mentions=mentions,
            image_uri=img,
            date=final_date,
            comments=total_comments,
            comments_content=comments,
            description=f_comment,
            likes=likes,
            relevance=0.01  # dev
        )

        posts.append(clean_p)

    end = time.time()

    print(f"scraping done | time: {(end-start)}")

    return posts
