from emitter.emit import emitter
from processor.core import launch_capturer
from storage import load_s3
from extrapolator import extractor

store = load_s3()

query = "cusco"

delay_seconds = 10*60
period_seconds = 10*60

t, q = extractor(store, query, delay_seconds, period_seconds)
t.start()

p, pq = launch_capturer(q)
p.start()

e = emitter(pq, delay_seconds)
e.start()
