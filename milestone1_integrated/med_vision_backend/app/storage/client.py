import boto3
from app.core.config import settings

PUBLIC_BASE_URL = "https://storage.medviss.in"
INTERNAL_ENDPOINT = "http://localhost:9000"

class StorageClient:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            endpoint_url=INTERNAL_ENDPOINT,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
        )
        self.bucket = settings.s3_bucket_name

    def upload_file(self, file_obj, key: str, content_type: str = None) -> str:
        extra_args = {"ContentType": content_type} if content_type else {}
        self.client.upload_fileobj(file_obj, self.bucket, key, ExtraArgs=extra_args)
        return f"{PUBLIC_BASE_URL}/{self.bucket}/{key}"

    def get_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        return f"{PUBLIC_BASE_URL}/{self.bucket}/{key}"

    def download_file(self, key: str, local_path: str):
        self.client.download_file(self.bucket, key, local_path)

storage_client = StorageClient()