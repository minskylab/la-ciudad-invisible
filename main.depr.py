from queue import Queue
from threading import Thread
from database import load_arango
from storage import load_s3
from extrapolator import extractor


def process(queue: Queue):
    while True:
        val = queue.get()
        print(val)
        queue.task_done()


db = load_arango()
store = load_s3()

query = "cusco"

delay_seconds = 60
period_seconds = 60

t, q = extractor(store, db, query, delay_seconds, period_seconds)
t.start()

p = Thread(target=process, args=(q,), daemon=True)
p.start()
