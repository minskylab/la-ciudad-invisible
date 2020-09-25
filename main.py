from ferret.scraper import extractor
from emitter.emit import emitter_app
from processor.core import launch_capturer
from storage import load_s3


store = load_s3()

query = "cusco"

delay_seconds = 10*60
period_seconds = 10*60

t, q = extractor(store, query, delay_seconds, period_seconds)
t.start()

p, pq = launch_capturer(q)
p.start()

e, app, socketio = emitter_app(pq, delay_seconds)
e.start()

socketio.run(app, host="0.0.0.0")
