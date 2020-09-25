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
        "date": p.date,
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
        test1 = {"id": "test1", "relevance": 0.34, "sentiment": 0.52}
        test2 = {"id": "test2", "relevance": 0.34, "sentiment": 0.35}

        Timer(10, emit_new_post, args=(test1,)).start()
        Timer(20, emit_new_post, args=(test2,)).start()

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
