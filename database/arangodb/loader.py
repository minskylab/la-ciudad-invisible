import os
from arango import ArangoClient


def load_arango():
    endpoint = os.getenv("ARANGO_ENDPOINT", "http://127.0.0.1:8529")
    username = os.getenv("ARANGO_USERNAME", "root")
    password = os.getenv("ARANGO_PASSWORD", "")
    db_name = os.getenv("ARANGO_DATABASE", "laciudadinvisible")

    client = ArangoClient(hosts=endpoint)

    # Connect to "_system" database as root user.
    sys_db = client.db('_system', username=username, password=password)

    try:
        sys_db.create_database(db_name)
    except:
        print("probably the database already exists")

    db = client.db(db_name, username=username, password=password)

    return db
