import boto3
from botocore.exceptions import ClientError


class QSecret:
    def __init__(
        self, aws_access_key_id, aws_secret_access_key, region_name="us-east-1"
    ):
        region_name = "us-east-1"

        # Create a Secrets Manager client
        self.session = boto3.session.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )
        self.client = self.session.client(
            service_name="secretsmanager",
            region_name=region_name,
        )

    def get(self, secret_name):
        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            raise e

        # Decrypts secret using the associated KMS key.
        secret = get_secret_value_response["SecretString"]
        return secret
