import time
from datetime import datetime, timedelta
from threading import Thread, Timer
from typing import Tuple
from database.postgres.ents import Post
from queue import Queue
from flask_socketio import SocketIO, emit
from flask import copy_current_request_context, Flask, render_template
from random import random


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

            Timer(30, emit_new_post, args=(test1,)).start()
            Timer(70, emit_new_post, args=(test2,)).start()
            Timer(100, emit_new_post, args=(test3,)).start()
            Timer(140, emit_new_post, args=(test4,)).start()
            Timer(200, emit_new_post, args=(test5,)).start()

            time.sleep(200)

    def sub(pq: Queue, delay_seconds: int):
        while True:
            val: Post = pq.get()

            actual_date = val.date + timedelta(seconds=delay_seconds)
            dist = datetime.now() - actual_date
            time_to_launch = float(delay_seconds - dist.seconds)

            d_post = post_to_event(val)

            Timer(time_to_launch, emit_new_post, args=(d_post,)).start()

    def emitter(pq: Queue, delay_seconds: int) -> Thread:
        return Thread(target=sub, args=(pq, delay_seconds), daemon=True)

    # demo activated
    Thread(target=demo_mode, daemon=True).start()

    return emitter(pq, delay_seconds), app, socketio
