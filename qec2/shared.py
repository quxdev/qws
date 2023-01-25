import boto3
import os


class QEC2:
    def __init__(self, region_name):
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

        self.ec2 = boto3.resource(
            "ec2",
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    def instances(self):
        try:
            return [self.instance(x.id) for x in self.ec2.instances.all()]
        except Exception as e:
            print(e)
            return None

    def instance(self, id):
        try:
            i = self.ec2.Instance(id)
            d = {"id": i.id, "state": i.state["Name"], "cpu": i.cpu_options}
            for t in i.tags:
                if t["Key"] in ["Name", "known_as", "domain", "service"]:
                    d[t["Key"]] = t["Value"]
            return d
        except Exception as e:
            print(e)
            return None

    def start(self, id):
        try:
            instance = self.ec2.Instance(id)
            if instance.state["Name"] == "running":
                print(f"Instance {id} is already running")
                return False
            instance.start()
            return True
        except Exception as e:
            print(e)
            return None

    def stop(self, id):
        try:
            instance = self.ec2.Instance(id)
            if instance.state["Name"] != "running":
                print(f"Instance {id} is not running")
                return False
            instance.stop()
            return True
        except Exception as e:
            print(e)
            return None

    def state(self, id):
        try:
            instance = self.ec2.Instance(id)
            return instance.state["Name"]
        except Exception as e:
            print(e)
            return None
