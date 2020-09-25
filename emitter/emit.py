from datetime import datetime, timedelta
from threading import Thread, Timer
from typing import Tuple
from database.postgres.ents import Post
from queue import Queue
from flask_socketio import SocketIO, emit
from flask import copy_current_request_context, Flask, render_template


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

    @socketio.on('handshake')
    def handle_my_custom_event(json):
        print('received json: ' + str(json))

    @app.route('/')
    def index():
        return render_template("index.html")

    # @copy_current_request_context
    def emit_new_post(post: dict):
        print(post["id"], post["relevance"], post["sentiment"])

        # data = post_to_event(post)
        socketio.emit("new post", post)

    def sub(pq: Queue, delay_seconds: int):
        img1 = "/static/CFi7iK7l4EX.jpg"
        img2 = "/static/CFi5prRJrIB.jpg"
        img3 = "/static/CFi5rIslLVU.jpg"
        img4 = "/static/CFi5v8-gh00.jpg"
        img5 = "/static/CFi6HdBnuEa.jpg"

        test1 = {"id": "test1", "relevance": 0.34,
                 "sentiment": 0.52, "image": img1}

        test2 = {"id": "test2", "relevance": 0.34,
                 "sentiment": 0.35, "image": img2}

        test3 = {"id": "test3", "relevance": 0.50,
                 "sentiment": 0.35, "image": img3}

        test4 = {"id": "test4", "relevance": 0.50,
                 "sentiment": 0.35, "image": img4}

        test5 = {"id": "test4", "relevance": 0.50,
                 "sentiment": 0.35, "image": img5}

        Timer(30, emit_new_post, args=(test1,)).start()
        Timer(70, emit_new_post, args=(test2,)).start()
        Timer(100, emit_new_post, args=(test3,)).start()
        Timer(140, emit_new_post, args=(test4,)).start()
        Timer(200, emit_new_post, args=(test5,)).start()

        while True:
            val: Post = pq.get()

            actual_date = val.date + timedelta(seconds=delay_seconds)
            dist = datetime.now() - actual_date
            time_to_launch = float(delay_seconds - dist.seconds)

            d_post = post_to_event(val)

            Timer(time_to_launch, emit_new_post, args=(d_post,)).start()

    def emitter(pq: Queue, delay_seconds: int) -> Thread:
        return Thread(target=sub, args=(pq, delay_seconds), daemon=True)

    return emitter(pq, delay_seconds), app, socketio
