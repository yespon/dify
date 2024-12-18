from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class SohuOSSStorageConfig(BaseSettings):
    """
    Configuration settings for Sohu OSS object storage
    """

    SOHU_OSS_BUCKET_NAME: Optional[str] = Field(
        description="Name of the Sohu OSS bucket to store and retrieve objects",
        default=None,
    )

    SOHU_OSS_ACCESS_KEY_ID: Optional[str] = Field(
        description="Access key ID for authenticating with the Sohu OSS service",
        default=None,
    )

    SOHU_OSS_ACCESS_KEY_SECRET: Optional[str] = Field(
        description="Secret access key for authenticating with the Sohu OSS service",
        default=None,
    )
