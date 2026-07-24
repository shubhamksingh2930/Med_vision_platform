import json
import logging
import aiobotocore.session
from fastapi import UploadFile
from app.core.config import settings

logger = logging.getLogger(__name__)

class R2Service:
    def __init__(self):
        self.session = aiobotocore.session.get_session()

    def _get_client(self):
        return self.session.create_client(
            's3',
            endpoint_url=settings.R2_ENDPOINT_URL,
            aws_access_key_id=settings.R2_ACCESS_KEY_ID,
            aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
        )

    async def ensure_bucket_exists(self):
        """Ensures target S3 / MinIO bucket exists."""
        try:
            async with self._get_client() as client:
                buckets = await client.list_buckets()
                bucket_names = [b['Name'] for b in buckets.get('Buckets', [])]
                if settings.R2_BUCKET_NAME not in bucket_names:
                    await client.create_bucket(Bucket=settings.R2_BUCKET_NAME)
                    logger.info(f"Created bucket '{settings.R2_BUCKET_NAME}'")
        except Exception as e:
            logger.warning(f"Could not auto-create bucket '{settings.R2_BUCKET_NAME}': {e}")

    async def upload_bytes(self, file_bytes: bytes, destination_key: str, content_type: str) -> str:
        """Upload raw byte array to storage."""
        async with self._get_client() as client:
            await client.put_object(
                Bucket=settings.R2_BUCKET_NAME,
                Key=destination_key,
                Body=file_bytes,
                ContentType=content_type
            )
            return destination_key

    async def upload_binary_stream(self, file: UploadFile, destination_key: str) -> str:
        """Uploads an UploadFile stream or file-like object to storage."""
        contents = await file.read()
        content_type = file.content_type or "application/octet-stream"
        return await self.upload_bytes(
            file_bytes=contents,
            destination_key=destination_key,
            content_type=content_type
        )

    async def upload_json(self, data: dict, destination_key: str) -> str:
        """Uploads JSON log metadata directly to storage."""
        json_bytes = json.dumps(data, indent=2).encode("utf-8")
        return await self.upload_bytes(
            file_bytes=json_bytes,
            destination_key=destination_key,
            content_type="application/json"
        )

    async def upload_json_log(self, data: dict, destination_key: str) -> str:
        """Alias for upload_json required by upload endpoint."""
        return await self.upload_json(data=data, destination_key=destination_key)

    async def get_object_bytes(self, destination_key: str) -> bytes:
        """Retrieves object raw bytes from storage."""
        async with self._get_client() as client:
            response = await client.get_object(
                Bucket=settings.R2_BUCKET_NAME,
                Key=destination_key
            )
            async with response['Body'] as stream:
                return await stream.read()

r2_service = R2Service()
