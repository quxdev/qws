import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from boto3 import client as aws_client


class AWSEmail(object):
    def __init__(self):
        self.sender = "qux@quxdev.com"
        self.to = None
        self.cc = None
        self.bcc = None
        self.subject = None
        self.message = None
        self.files = None

        access_key = os.getenv("AWS_SES_ACCESS_KEY", None)
        secret_key = os.getenv("AWS_SES_SECRET_KEY", None)
        aws_region = os.getenv("AWS_SES_REGION", "us-east-1")

        # Backwards compatibility for old ENV variables
        access_key = os.getenv("AWS_SES_ACCESS_KEY_ID", access_key)
        secret_key = os.getenv("AWS_SES_SECRET_ACCESS_KEY", secret_key)
        aws_region = os.getenv("AWS_REGION", aws_region)

        self.client = aws_client(
            service_name="ses",
            region_name=aws_region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    @staticmethod
    def destination_header(value):
        if type(value) is str:
            return value
        if type(value) is list:
            return ",".join(value)
        return

    @staticmethod
    def destination_aslist(*args):
        result = []
        for arg in args:
            if type(arg) is str:
                result.extend([arg])
            if type(arg) is list:
                result.extend(arg)
        return result

    @staticmethod
    def getattachment(filename):
        if not os.path.exists(filename):
            return None

        part = MIMEApplication(
            open(filename, "rb").read(), filename=os.path.basename(filename)
        )
        part.add_header(
            "Content-Disposition", "attachment", filename=os.path.basename(filename)
        )
        # part.set_type()
        return part

    def send(self):
        if self.client is None:
            return
        if self.subject is None:
            return
        if self.message is None:
            return
        if self.to is None:
            return

        message = MIMEMultipart()

        message["Subject"] = self.subject
        message["From"] = self.sender

        if self.to:
            message["To"] = self.destination_header(self.to)
        if self.cc:
            message["Cc"] = self.destination_header(self.cc)
        if self.bcc:
            message["Bcc"] = self.destination_header(self.bcc)

        part = MIMEText(self.message, "html", "utf-8")
        message.attach(part)

        if self.files:
            if type(self.files) is not list:
                self.files = [self.files]
            for file in self.files:
                attachment = self.getattachment(file)
                if attachment:
                    message.attach(attachment)
                else:
                    print(f"Cannot attach file:{file}")

        rawmessage = dict(Data=message.as_string())
        response = self.client.send_raw_email(
            Destinations=self.destination_aslist(self.to, self.cc, self.bcc),
            Source=self.sender,
            RawMessage=rawmessage,
        )
        return message, response


def test_aws():
    filename = "SPY.csv"

    foo = AWSEmail()
    foo.to = "qux@quxdev.com"
    foo.cc = "abc@quxdev.com"
    foo.bcc = "def@quxdev.com"
    foo.files = filename
    foo.subject = "RACECAR..."
    foo.message = "...is a palindrome!"
    message, response = foo.send()
    print(message)
    print(response)


if __name__ == "__main__":
    test_aws()
