### Accessing secrets - key, value pair from AWS Secrets Manager

## 1 Install Dependencies if not installed already
```
pip install boto3

## Usage
You will need the aws keys that have permissions to these secrets
Use the get with the name of the secret to access the key/value pair
```
qsecret_obj = QSecret(aws_access_key_id, aws_secret_key, region)
result = qsecret_obj.get("test/secret")

```
result will be a json {"test-secret" : "Testing"}