from dataclasses import dataclass
import boto3
import botocore
from io import BytesIO
import gzip


@dataclass(frozen=True)
class S3Config:
    aws_access_key_id: str = None
    aws_secret_access_key: str = None

    @property
    def client(self):
        client = boto3.client(
            "s3",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )
        return client


class S3path:
    def __init__(self, *args) -> None:
        if len(args) == 1:
            path = args[0]
            self.path = path
            self.bucket, *filekeys = path.replace("s3://", "").split("/")
            self.key = "/".join(filekeys)
        elif len(args) == 2:
            bucket, key = args
            self.bucket = bucket
            self.key = key
            self.path = f"s3://{bucket}/{key}"
        else:
            raise ValueError("Invalid number of arguments")

    @property
    def is_zip(self):
        return self.key.endswith(".zip")

    @property
    def is_gzip(self):
        return self.key.endswith(".gz")


class Q3:
    def __init__(self, config: S3Config) -> None:
        self.config = config

    def list(self, path: S3path) -> list:
        try:
            response = self.config.client.list_objects_v2(
                Bucket=path.bucket, Prefix=path.key
            )
            return [S3path(path.bucket, x["Key"]) for x in response["Contents"]]
        except Exception as e:
            print(e)
            return []

    def exists(self, path: S3path) -> bool:
        try:
            self.config.client.head_object(Bucket=path.bucket, Key=path.key)
            return True
        except botocore.exceptions.ClientError:
            return False

    def download(self, path: S3path) -> BytesIO:
        buffer = BytesIO()
        try:
            self.config.client.download_fileobj(path.bucket, path.key, buffer)
            buffer.seek(0)
            if path.is_gzip:
                decompressed_data = gzip.decompress(buffer.read())
                return BytesIO(decompressed_data)
            return buffer
        except Exception as e:
            print(e)
            return None

    def upload(self, path: S3path, data: BytesIO) -> bool:
        if path.is_gzip:
            return self.__upload_gzip(path, data)
        else:
            return self.__upload_file(path, data)

    def __upload_file(self, path: S3path, data: BytesIO) -> bool:
        try:
            self.config.client.upload_fileobj(data, path.bucket, path.key)
            return True
        except Exception as e:
            print(e)
            return None

    def __upload_gzip(self, path: S3path, data: BytesIO) -> bool:
        try:
            compressed_data = gzip.compress(data.getvalue())
            self.config.client.upload_fileobj(
                BytesIO(compressed_data),
                path.bucket,
                path.key,
                ExtraArgs={"ContentEncoding": "gzip", "ContentType": "text/csv"},
            )
            return True
        except Exception as e:
            print(e)
            return None
