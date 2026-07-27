import boto3
from app.core.config import settings

class StorageClient:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.s3_endpoint_url,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
        )
        self.bucket = settings.s3_bucket_name

    def upload_file(self, file_obj, key: str, content_type: str = None) -> str:
        extra_args = {"ContentType": content_type} if content_type else {}
        self.client.upload_fileobj(file_obj, self.bucket, key, ExtraArgs=extra_args)
        return f"{settings.s3_endpoint_url}/{self.bucket}/{key}"

    def get_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        return self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": key},
            ExpiresIn=expires_in,
        )

storage_client = StorageClient()