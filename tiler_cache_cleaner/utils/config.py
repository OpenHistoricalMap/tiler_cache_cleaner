import os
import boto3


class Config:
    TILER_CACHE_AWS_ACCESS_KEY_ID = os.getenv("TILER_CACHE_AWS_ACCESS_KEY_ID", "")
    TILER_CACHE_AWS_SECRET_ACCESS_KEY = os.getenv("TILER_CACHE_AWS_SECRET_ACCESS_KEY", "")
    TILER_CACHE_AWS_ENDPOINT = os.getenv("TILER_CACHE_AWS_ENDPOINT", "https://s3.amazonaws.com")
    TILER_CACHE_REGION = os.getenv("TILER_CACHE_REGION", "us-east-1")  # us-east-1 or hel1
    bucket_name = os.getenv("TILER_CACHE_BUCKET", "none")

    @staticmethod
    def get_s3_client():
        return boto3.client(
            "s3",
            aws_access_key_id=Config.TILER_CACHE_AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.TILER_CACHE_AWS_SECRET_ACCESS_KEY,
            endpoint_url=Config.TILER_CACHE_AWS_ENDPOINT,
            region_name=Config.TILER_CACHE_REGION,
        )
