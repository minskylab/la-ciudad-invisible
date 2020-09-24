from datetime import datetime, timedelta
from threading import Thread
from database.postgres.ents import Post
from queue import Queue


def sub(pq: Queue, delay_seconds: int):
    while True:
        val: Post = pq.get()
        print(f"emitting [{val.post_id}]")
        actual_date = val.date + timedelta(seconds=delay_seconds)
        dist = datetime.now() - actual_date
        print(dist)


def emitter(pq: Queue, delay_seconds: int) -> Thread:
    return Thread(target=sub, args=(pq, delay_seconds), daemon=True)
