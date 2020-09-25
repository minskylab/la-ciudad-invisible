from datetime import datetime, timedelta
from threading import Thread, Timer
from database.postgres.ents import Post
from queue import Queue
from flask_socketio import emit


def post_to_event(p: Post) -> dict:
    return {
        "id": p.post_id,
        "date": p.date,
        "image": p.image_uri,
        "description": p.description,
        "sentiment": p.sentiment,
        "relevance": p.relevance,
    }


def emit(post: Post):
    print(post.post_id, post.relevance, post.sentiment)

    data = post_to_event(post)
    emit("new_event", data, broadcast=True)


def sub(pq: Queue, delay_seconds: int):

    while True:
        val: Post = pq.get()
        actual_date = val.date + timedelta(seconds=delay_seconds)
        dist = datetime.now() - actual_date
        time_to_launch = float(delay_seconds - dist.seconds)
        Timer(time_to_launch, emit, args=(val,)).start()


def emitter(pq: Queue, delay_seconds: int) -> Thread:
    return Thread(target=sub, args=(pq, delay_seconds), daemon=True)
