from datetime import datetime, timedelta
from threading import Thread, Timer
from database.postgres.ents import Post
from queue import Queue


def emition(post: Post):
    print(post)


def sub(pq: Queue, delay_seconds: int):
    while True:
        val: Post = pq.get()
        actual_date = val.date + timedelta(seconds=delay_seconds)
        dist = datetime.now() - actual_date
        print(dist.seconds)
        Timer(float(dist.seconds), emition, args=(val,))


def emitter(pq: Queue, delay_seconds: int) -> Thread:
    return Thread(target=sub, args=(pq, delay_seconds), daemon=True)
