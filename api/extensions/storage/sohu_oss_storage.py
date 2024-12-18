import collections
import io
import logging
import sys
from collections.abc import Generator

sys.modules['collections'].Callable = collections.abc.Callable
from vulpo.scs.connection import SCSConnection

from configs import dify_config
from extensions.storage.base_storage import BaseStorage

logger = logging.getLogger(__name__)


class SohuOssStorage(BaseStorage):
    """Implementation for Sohu Oss storage."""

    def __init__(self):
        super().__init__()
        self.bucket_name = dify_config.SOHU_OSS_BUCKET_NAME
        self.client = SCSConnection(
            aws_access_key_id=dify_config.SOHU_OSS_ACCESS_KEY_ID,
            aws_secret_access_key=dify_config.SOHU_OSS_ACCESS_KEY_SECRET
        )
        
        # create bucket
        try:
            self.bucket = self.client.get_bucket(self.bucket_name)
            if not self.bucket:
                self.bucket = self.client.create_bucket(self.bucket_name)
        except Exception as e:
            raise

    def save(self, filename, data):
        key = self.bucket.new_key(filename)
        if isinstance(data, str):
            data = data.encode('utf-8')
        fp = io.BytesIO(data)
        key.set_contents_from_file(fp)
        fp.close()

    def load_once(self, filename: str) -> bytes:
        try:
            key = self.bucket.get_key(filename)
            fp = io.BytesIO()
            key.get_contents_to_file(fp)
            data = fp.getvalue()
            fp.close()
        except Exception as e:
            if not key:
                raise FileNotFoundError("File not found")
            raise

        return data

    def load_stream(self, filename: str) -> Generator:
        try:
            key = self.bucket.get_key(filename)
            while chunk := key.get_contents_as_string():
                yield chunk
        except Exception as e:
            if not key:
                raise FileNotFoundError("File not found")
            raise

    def download(self, filename, target_filepath):
        try:
            key = self.bucket.get_key(filename)
            key.get_contents_to_filename(target_filepath)
        except Exception as e:
            if not key:
                raise FileNotFoundError("File not found")
            raise

    def exists(self, filename):
        key = self.bucket.get_key(filename)
        if key:
            return True
        else:
            return False

    def delete(self, filename):
        self.bucket.delete_key(filename)
