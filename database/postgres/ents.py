import peewee as pw
from .base import BaseModel
import datetime


class Comment(BaseModel):
    message = pw.TextField()
    sentiment = pw.FloatField()


class Post(BaseModel):
    post_id = pw.TextField(index=True)
    image_uri = pw.TextField()
    description = pw.TextField()
    comments = pw.ManyToManyField(Comment, backref="post")
    date = pw.DateTimeField(default=datetime.datetime.now)
    hashtags = pw.TextField(default="")
    mentions = pw.TextField(default="")
    likes = pw.IntegerField(default=0)
    relevance = pw.FloatField(default=0.0)
    sentiment = pw.FloatField(default=0.0)
    comments_sentiment = pw.FloatField(default=0.0)
    comments_count = pw.IntegerField(default=0)


PostComments = Post.comments.get_through_model()
