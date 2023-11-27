from dataclasses import dataclass
from io import BytesIO
import zipfile
import gzip
import os
import boto3
import botocore


@dataclass(frozen=True)
class S3Config:
    aws_access_key_id: str = None
    aws_secret_access_key: str = None
    cache_active: bool = False
    cache_dir: str = None

    @property
    def client(self):
        client = boto3.client(
            "s3",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )
        return client

    @property
    def cache_enabled(self):
        return self.cache_active and self.cache_dir and os.path.exists(self.cache_dir)


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

    # ------- new methods for q3min ------- with cache and zip support

    def download_v2(self, spath: S3path) -> list:
        path = os.path.join(self.config.cache_dir, spath.path.replace("s3://", ""))
        results = self.__from_cache(path)
        print(f"results from cache: {results}")
        if results:
            return results

        buffer = self.download(spath)
        if self.config.cache_enabled:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as f:
                if spath.is_gzip:
                    f.write(gzip.compress(buffer.read()))
                else:
                    f.write(buffer.read())
                buffer.seek(0)

        if spath.is_zip:
            _results = self.__unzip(buffer)
        else:
            _results = [{"filename": spath.path, "fileobj": buffer}]

        for r in _results:
            r["from"] = "s3"
            r["source"] = spath.path

        return _results

    def __from_cache(self, path: str) -> BytesIO:
        if self.config.cache_enabled and os.path.exists(path):
            with open(path, "rb") as f:
                buffer = BytesIO(f.read())
                buffer.seek(0)
            if path.endswith("zip"):
                results = self.__unzip(buffer)
            else:
                results = [{"filename": path, "fileobj": buffer}]

            for r in results:
                r["from"] = "cache"
                r["source"] = path

            return results

        return None

    def __unzip(self, file):
        results = []
        result = {}
        with zipfile.ZipFile(file) as zfile:
            for f in zfile.infolist():
                zf = zfile.open(f.filename)
                if zipfile.is_zipfile(zf):
                    _results = self.__unzip(zf)
                    results.extend(_results)
                else:
                    zf = zfile.open(f.filename)
                    buffer = BytesIO(zf.read())
                    buffer.seek(0)
                    if len(buffer.getvalue()) > 0:
                        result["filename"] = f.filename
                        result["fileobj"] = buffer
                        results.append(result.copy())

        print(f"unzipped: {results}")
        return results

    def list_cache(self, path: S3path) -> list:
        result = []
        if self.config.cache_enabled:
            path = os.path.join(self.config.cache_dir, path.path.replace("s3://", ""))
            dirname = os.path.dirname(path)
            if os.path.exists(path):
                for root, _, files in os.walk(dirname):
                    result.extend([os.path.join(root, f) for f in files])

        return result

    def exists_in_cache(self, path: S3path) -> bool:
        result = False
        if self.config.cache_enabled:
            path = os.path.join(self.config.cache_dir, path.path.replace("s3://", ""))
            result = os.path.exists(path)

        return result

    def upload_v2(self, path: S3path, data: BytesIO) -> bool:
        success = self.upload(path, BytesIO(data.getvalue()))

        print("success: ", success)
        if success and self.config.cache_enabled:
            localpath = os.path.join(
                self.config.cache_dir, path.path.replace("s3://", "")
            )
            os.makedirs(os.path.dirname(localpath), exist_ok=True)
            with open(localpath, "wb") as f:
                if path.is_gzip:
                    f.write(gzip.compress(data.getvalue()))
                else:
                    f.write(data.getvalue())

        return success
