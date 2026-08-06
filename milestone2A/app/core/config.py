from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Med-Vision Core API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # PostgreSQL Connection Parameters
    POSTGRES_USER: str = "med_user"
    POSTGRES_PASSWORD: str = "med_password"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "med_vision"

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @property
    def database_url(self) -> str:
        return self.DATABASE_URL

    # JWT Authentication Parameters
    SECRET_KEY: str = "CHANGE_THIS_TO_A_32_BYTE_SECRET_KEY_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # Storage (Cloudflare R2 / MinIO) Parameters
    R2_ACCOUNT_ID: str = "local"
    R2_ACCESS_KEY_ID: str = "minioadmin"
    R2_SECRET_ACCESS_KEY: str = "minioadmin"
    R2_BUCKET_NAME: str = "med-vision-bucket"
    S3_ENDPOINT_URL: str = "http://127.0.0.1:9000"

    @property
    def R2_ENDPOINT_URL(self) -> str:
        if self.R2_ACCOUNT_ID and self.R2_ACCOUNT_ID != "local":
            return f"https://{self.R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
        return self.S3_ENDPOINT_URL

    # Person B Storage Aliases
    @property
    def s3_endpoint_url(self) -> str: return self.R2_ENDPOINT_URL
    @property
    def s3_access_key(self) -> str: return self.R2_ACCESS_KEY_ID
    @property
    def s3_secret_key(self) -> str: return self.R2_SECRET_ACCESS_KEY
    @property
    def s3_bucket_name(self) -> str: return self.R2_BUCKET_NAME

    # Celery / Redis Settings
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()
