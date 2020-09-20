import os
import peewee as pw


host = os.getenv("PG_HOST", "localhost")
user = os.getenv("PG_USER", "postgres")
password = os.getenv("PG_PASSWORD", "")
db_name = os.getenv("PG_DATABASE", "laciudadinvisible")

db = pw.PostgresqlDatabase(
    db_name,
    host=host,
    user=user,
    password=password
)


class BaseModel(pw.Model):
    class Meta:
        database = db
