import boto3
import os


class Q3:
    """
    Q3 is a class that provides a wrapper around the s3 resource in boto3.
    It provides methods to list buckets, upload files, and list files in a bucket.
    """

    def __init__(self):
        aws_access_key_id = os.getenv("AWS_S3_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_S3_SECRET_ACCESS_KEY")
        self.s3 = boto3.resource(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    def list_buckets(self):
        try:
            buckets = self.s3.buckets.all()
            return [x.name for x in buckets.all()]

        except Exception as e:
            print(e)
            return None

    def set_bucket(self, bucket_name):
        if bucket_name in self.list_buckets():
            self.bucket = self.s3.Bucket(bucket_name)
        else:
            return None

    def upload_file(self, bucket_name, filename, filepath):

        if os.path.exists(filepath) is False:
            print(f"File not found: {filepath}")
            return None

        self.set_bucket(bucket_name)

        try:
            self.bucket.upload_file(filepath, filename)
            return True

        except Exception as e:
            print(e)
            return None

    # upload file like object - should be in binary format
    # open(filepath, "rb") will give you a file like object
    def upload_fileobj(self, bucket_name, filename, data):
        self.set_bucket(bucket_name)

        try:
            self.bucket.upload_fileobj(data, filename)
            return True

        except Exception as e:
            print(e)
            return None

    def list(self, bucket_name, prefix=""):
        self.set_bucket(bucket_name)

        try:
            if prefix and prefix > "":
                response = self.bucket.objects.filter(Prefix=prefix)
            else:
                response = self.bucket.objects.all()

            return [{"key": x.key, "last_modified": x.last_modified} for x in response]

        except Exception as e:
            print(e)
            return None
