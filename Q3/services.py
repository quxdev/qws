import s3fs
import pandas as pd
import os


class Q3:
    """
    Q3 is a class that provides a wrapper around the s3 resource in boto3.
    It provides methods to list buckets, upload files, and list files in a bucket.
    """

    def __init__(self):
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

        self.fs = s3fs.S3FileSystem(
            anon=False, key=aws_access_key_id, secret=aws_secret_access_key
        )

    def list(self, bucket, prefix=""):
        try:
            files = [
                self.fs.split_path(f)[1] for f in self.fs.find(bucket, prefix=prefix)
            ]
            return files
        except Exception as e:
            print(e)
            return None

    def get_df(self, fileurl):
        try:
            df = pd.read_csv(fileurl)
            return df
        except Exception as e:
            print(e)
            return None

    def upload_file(self, fileurl, filepath):
        try:
            self.fs.put(filepath, fileurl)
            return True
        except Exception as e:
            print(e)
            return None

    def upload_df(self, fileurl, df):
        try:
            df.to_csv(fileurl, index=False)
            return True
        except Exception as e:
            print(e)
            return None

    def exists(self, fileurl):
        try:
            return self.fs.exists(fileurl)
        except Exception as e:
            print(e)
            return None

    def put_tags(self, fileurl, tags, override=False):
        try:
            self.fs.put_tags(fileurl, tags, mode="o" if override else "m")
            return True
        except Exception as e:
            print(e)
            return None

    def get_tags(self, fileurl):
        try:
            return self.fs.get_tags(fileurl)
        except Exception as e:
            print(e)
            return None
