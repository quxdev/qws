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

The SAFE_MODE if set to True will send all emails to email ids listed in SAFE_MODE_TO only
- `SAFE_MODE` (True or False) - default True
- `SAFE_MODE_TO` (qux@quxdev.com,foo@quxdev.com)

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
