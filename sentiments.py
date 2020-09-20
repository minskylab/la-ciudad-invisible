from extrapolator.post import CleanPost
from database.postgres import Post, db, Comment
from queue import Queue
from threading import Thread
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from storage import load_s3
from extrapolator import extractor_loader


def process(queue: Queue):
    client = language.LanguageServiceClient()

    while True:
        val: CleanPost = queue.get()
        # print(f"from processor: {val}")
        queue.task_done()

        doc = types.Document(content=val.description,
                             type=enums.Document.Type.PLAIN_TEXT)
        sentiment = client.analyze_sentiment(document=doc).document_sentiment

        p = Post.create(
            post_id=val.id,
            image_uri=val.image_uri,
            description=val.description,
            date=val.date,
            likes=val.likes,
            hashtags=",".join(val.hashtags),
            mentions=",".join(val.mentions),
            relevance=val.relevance,
            sentiment=sentiment.score
        )

        for c in val.comments_content:
            doc = types.Document(
                content=c, type=enums.Document.Type.PLAIN_TEXT)
            sentiment = client.analyze_sentiment(
                document=doc).document_sentiment
            p.comments.add(Comment.create(
                message=c, sentiment=sentiment.score))

        # print(p)
        # print(f"Post {p.index} processed")


# arango_db = load_arango()
store = load_s3()

query = "cusco"

delay_seconds = 10*60
period_seconds = 10*60

t, q = extractor_loader(store, query, delay_seconds, period_seconds)
t.start()

p = Thread(target=process, args=(q,), daemon=True)
p.start()
