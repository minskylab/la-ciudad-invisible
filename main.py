from database import load_arango
from storage import load_s3

from extrapolator import extractor_loader


db = load_arango()
store = load_s3()

query = "cusco"

delay_hours = 2
period_seconds = 120

t, queue = extractor_loader(store, db, query, delay_hours, period_seconds)

t.start()
