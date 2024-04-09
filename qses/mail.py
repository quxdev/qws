import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from boto3 import client as aws_client


class AWSEmail:
    def __init__(self):
        self.sender = "qux@quxdev.com"
        self.to = None
        self.cc = None
        self.bcc = None
        self.subject = None
        self.message = None
        self.files = None
        self.client = self.set_client()

    def set_client(self):
        access_key = os.getenv("AWS_SES_ACCESS_KEY", None)
        secret_key = os.getenv("AWS_SES_SECRET_KEY", None)
        aws_region = os.getenv("AWS_SES_REGION", "us-east-1")

        # Backwards compatibility for old ENV variables
        access_key = os.getenv("AWS_SES_ACCESS_KEY_ID", access_key)
        secret_key = os.getenv("AWS_SES_SECRET_ACCESS_KEY", secret_key)
        aws_region = os.getenv("AWS_REGION", aws_region)

        if access_key and secret_key:
            client = aws_client(
                service_name="ses",
                region_name=aws_region,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
            )
            return client

        return None

    @staticmethod
    def destination_header(value):
        result = value
        if isinstance(value, list):
            stripped_value = [x.strip() for x in value]
            result = ",".join(stripped_value)
        return result

    @staticmethod
    def destination_aslist(*args):
        result = []
        for arg in args:
            if isinstance(arg, str):
                new_args = arg.split(",")
                result.extend(new_args)
            elif isinstance(arg, list):
                result.extend(arg)

        return result

    @staticmethod
    def getattachment(filepath):
        if not os.path.exists(filepath):
            return None

        with open(filepath, "rb") as f:
            filedata = f.read()
            filename = os.path.basename(filepath)
            part = MIMEApplication(filedata, filename)
        part.add_header("Content-Disposition", "attachment", filename=filename)
        return part

    def send(self):
        if not any([self.client, self.subject, self.message, self.to]):
            print("Missing one or more of the following: client, subject, message, to")
            print(f"client : {self.client}")
            print(f"subject: {self.subject}")
            print(f"message: {self.message}")
            print(f"to     : {self.to}")

            return False

        message = MIMEMultipart()

        message["Subject"] = self.subject
        message["From"] = self.sender

        to, cc, bcc = self.set_receipients(self.to, self.cc, self.bcc)

        message["To"] = to
        message["Cc"] = cc
        message["Bcc"] = bcc

        if not message["To"]:
            print(f"Missing To: {message['To']}")
            print(f"SAFE_MODE: {os.getenv('SAFE_MODE', 'True')}")
            print(f"SAFE_MODE_TO: {os.getenv('SAFE_MODE_TO', None)}")
            return False

        part = MIMEText(self.message, "html", "utf-8")
        message.attach(part)

        if self.files:
            if not isinstance(self.files, list):
                self.files = [self.files]

            for file in self.files:
                attachment = self.getattachment(file)
                if attachment:
                    message.attach(attachment)
                else:
                    print(f"Cannot attach file:{file}")

        rawmessage = {"Data": message.as_string()}

        response = self.client.send_raw_email(
            Destinations=self.destination_aslist(to, cc, bcc),
            Source=self.sender,
            RawMessage=rawmessage,
        )

        if (
            response
            and response["ResponseMetadata"]
            and response["ResponseMetadata"]["HTTPStatusCode"] != 200
        ):
            print(
                f"Failed to send email: status={response['ResponseMetadata']['HTTPStatusCode']}"
            )
            return False

        return True

    def set_receipients(self, to, cc, bcc):
        safe_mode = os.getenv("SAFE_MODE", "True").lower() == "true"
        safe_mode_args = os.getenv("SAFE_MODE_TO", None)
        recepient_to = None
        recepient_cc = None
        recepient_bcc = None

        if not safe_mode:
            recepient_to = self.destination_header(to)
            recepient_cc = self.destination_header(cc)
            recepient_bcc = self.destination_header(bcc)
        elif safe_mode_args:
            recepient_to = self.destination_header(safe_mode_args)

        print(f"SAFE_MODE: {safe_mode}")
        print(f"SAFE_MODE_TO: {safe_mode_args}")
        print(f"recepient_to: {recepient_to}")
        print(f"recepient_cc: {recepient_cc}")
        print(f"recepient_bcc: {recepient_bcc}")

        return recepient_to, recepient_cc, recepient_bcc


def main():
    from dotenv import load_dotenv

    load_dotenv()

    testemail = AWSEmail()
    testemail.sender = "noreply@batteryos.com"
    testemail.to = "qux@quxdev.com"
    testemail.cc = "abc@quxdev.com"
    testemail.bcc = "def@quxdev.com"
    testemail.subject = "RACECAR..."
    testemail.message = "...is a palindrome!"
    response = testemail.send()

    print(f"message sent: {response}")


if __name__ == "__main__":
    main()
