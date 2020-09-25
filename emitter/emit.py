from datetime import datetime, timedelta
from threading import Thread, Timer
from database.postgres.ents import Post
from queue import Queue


def emit(post: Post):
    print(post.post_id, post.sentiment)


def sub(pq: Queue, delay_seconds: int):
    while True:
        val: Post = pq.get()
        actual_date = val.date + timedelta(seconds=delay_seconds)
        dist = datetime.now() - actual_date
        time_to_launch = float(delay_seconds - dist.seconds)
        Timer(time_to_launch, emit, args=(val,)).start()


def emitter(pq: Queue, delay_seconds: int) -> Thread:
    return Thread(target=sub, args=(pq, delay_seconds), daemon=True)
