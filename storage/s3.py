import os
from minio import Minio


def load_s3() -> Minio:
    endpoint = os.getenv("S3_ENDPOINT", "")
    access_key = os.getenv("S3_ACCESS_KEY", "")
    secret_key = os.getenv("S3_SECRET_KEY", "")
    bucket = os.getenv("S3_BUCKET", "")
    ssl = os.getenv("S3_SSL", True)
    region = os.getenv("S3_REGION", "")

    m_client = Minio(endpoint,
                     access_key=access_key,
                     secret_key=secret_key,
                     secure=ssl,
                     region=region
                     )

    if not m_client.bucket_exists(bucket):
        m_client.make_bucket(bucket)

    return m_client
