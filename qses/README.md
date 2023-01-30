# qses - Wrapper for AWS SES send mail

## Dependencies
1. boto3
2. dotenv is required in your django project as it will access env variables

## Install
1. install dependencies
```
pip install boto3
```

2. Add the following to your .env file
    AWS_SES_ACCESS_KEY_ID = ""
    AWS_SES_SECRET_ACCESS_KEY = ""
    AWS_REGION = ""

## Usage

```

filename = "/Users/psathaye/Downloads/mapping.csv"

foo = AWSEmail()
foo.to = "parag@finmachines.com"
foo.cc = "parag@finmachines.net"
foo.bcc = foo.cc
foo.files = filename
foo.subject = "TESTING QSES EMAIL"
foo.message = "TESTING QSES EMAIL ..."
message, response = foo.send()
print(message)
print(response)

```
