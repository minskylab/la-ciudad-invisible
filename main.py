from extrapolator.post import CleanPost
from database.postgres import Post, Comment
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

        comments_sentiment = []
        for c in val.comments_content:
            doc = types.Document(
                content=c,
                type=enums.Document.Type.PLAIN_TEXT,
            )

            sentiment = client.analyze_sentiment(
                document=doc).document_sentiment

            p.comments.add(Comment.create(
                message=c, sentiment=sentiment.score))

            comments_sentiment.append(sentiment.score)

        if len(comments_sentiment) > 0:
            mean_sentiment = sum(comments_sentiment)/len(comments_sentiment)
        else:
            mean_sentiment = 0

        Post.update(comments_sentiment=mean_sentiment).where(
            Post.post_id == val.id).execute()

        Post.update(comments_count=len(comments_sentiment)).where(
            Post.post_id == val.id).execute()

        # print(p)
        # print(f"Post {p.index} processed")


store = load_s3()

query = "cusco"

delay_seconds = 10*60
period_seconds = 10*60

t, q = extractor_loader(store, query, delay_seconds, period_seconds)
t.start()

p = Thread(target=process, args=(q,), daemon=True)
p.start()
