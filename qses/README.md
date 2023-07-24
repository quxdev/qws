# QSES

> Wrapper for AWS SES send mail aka QWS SES

## Dependencies

1. boto3
2. dotenv is required in your django project as it will access env variables

## Install

```
pip install boto3
```

## Configure

Add the following to your .env file

- `AWS_SES_ACCESS_KEY` (_AWS Access Key ID_)
- `AWS_SES_SECRET_KEY` (_AWS Secret Access Key_)
- `AWS_SES_REGION` (_AWS Region_)

## Usage

```
foo = AWSEmail()

foo.to = "qws@quxdev.com"
foo.cc = "cc@quxdev.com"
foo.bcc = "bcc@quxdev.com"

filename = "SPY.csv"
foo.files = filename

foo.subject = "TESTING QSES EMAIL"

foo.message = "TESTING QSES EMAIL ..."

message, response = foo.send()
print(message)
print(response)
```
