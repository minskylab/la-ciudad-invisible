import os
import time
from datetime import datetime, timedelta
from threading import Thread, Timer
from typing import Tuple
from database.postgres.ents import Post
from queue import Queue
from flask_socketio import SocketIO, emit
from flask import copy_current_request_context, Flask, render_template
from random import choice, random


def post_to_event(p: Post) -> dict:
    return {
        "id": p.post_id,
        "date": str(p.date),
        "image": p.image_uri,
        "description": p.description,
        "sentiment": p.sentiment,
        "relevance": p.relevance,
    }


def emitter_app(pq: Queue, delay_seconds: int) -> Tuple[Thread, Flask, SocketIO]:
    app = Flask("la-ciudad-invisible")
    app.config['SECRET_KEY'] = 'secret!'

    socketio = SocketIO(app)
    socketio.init_app(app, cors_allowed_origins="*")

    @socketio.on('handshake')
    def handle_my_custom_event(json):
        print('received json: ' + str(json))

    @app.route('/')
    def index():
        return render_template("index.html")

    # @copy_current_request_context
    def emit_new_post(post: dict):
        print(post["id"], post["relevance"], post["image"])

        # data = post_to_event(post)
        socketio.emit("new post", post)

    def demo_mode():
        img1 = "/static/CFi7iK7l4EX.jpg"
        img2 = "/static/CFi5prRJrIB.jpg"
        img3 = "/static/CFi5rIslLVU.jpg"
        img4 = "/static/CFi5v8-gh00.jpg"
        img5 = "/static/CFi6HdBnuEa.jpg"
        img6 = "/static/CFi5wUZJIMa.jpg"
        img7 = "/static/CFi6bObAd1k.jpg"
        img8 = "/static/CFi-EXkAHbU.jpg"

        while True:
            test1 = {"id": "demo_01", "relevance": random(),
                     "sentiment": 0.52, "image": img1}

            test2 = {"id": "demo_02", "relevance": random(),
                     "sentiment": 0.35, "image": img2}

            test3 = {"id": "demo_03", "relevance": random(),
                     "sentiment": 0.35, "image": img3}

            test4 = {"id": "demo_04", "relevance": random(),
                     "sentiment": 0.35, "image": img4}

            test5 = {"id": "demo_05", "relevance": random(),
                     "sentiment": 0.35, "image": img5}

            test6 = {"id": "demo_06", "relevance": random(),
                     "sentiment": 0.35, "image": img6}

            test7 = {"id": "demo_07", "relevance": random(),
                     "sentiment": 0.35, "image": img7}

            test8 = {"id": "demo_08", "relevance": random(),
                     "sentiment": 0.35, "image": img8}

            tests = [test1, test2, test3, test4, test5, test6, test7, test8]

            timer = random() * 135 + 35
            t = choice(tests)

            Timer(timer, emit_new_post, args=(t,)).start()

            time.sleep(30)

    def sub(pq: Queue, delay_seconds: int):
        while True:
            val: Post = pq.get()
            actual_date = val.date + timedelta(seconds=delay_seconds)

            if os.getenv("PROD", False):
                now = datetime.now() - timedelta(hours=5)
            else:
                now = datetime.now()

            dist = now - actual_date
            time_to_launch = float(delay_seconds - dist.seconds)

            d_post = post_to_event(val)

            Timer(time_to_launch, emit_new_post, args=(d_post,)).start()

    def emitter(pq: Queue, delay_seconds: int) -> Thread:
        return Thread(target=sub, args=(pq, delay_seconds), daemon=True)

    # demo deactivated
    # Thread(target=demo_mode, daemon=True).start()

    return emitter(pq, delay_seconds), app, socketio
