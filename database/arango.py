import os
from pyArango.connection import Connection, Database


def load_arango() -> Database:
    endpoint = os.getenv("ARANGO_ENDPOINT", "http://127.0.0.1:8529")
    username = os.getenv("ARANGO_USERNAME", "root")
    password = os.getenv("ARANGO_PASSWORD", "root")
    db_name = os.getenv("ARANGO_DATABASE", "laciudadinvisible")

    conn = Connection(arangoURL=endpoint, username=username, password=password)

    db: Database = None
    if db_name not in conn:
        db = conn.createDatabase(db_name)
    else:
        db = conn[db_name]

    return db
