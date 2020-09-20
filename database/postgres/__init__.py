from .base import db, BaseModel
from .ents import Post, Comment, PostComments


db.create_tables([Post, Comment, PostComments])
