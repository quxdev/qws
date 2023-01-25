# qec2 - Manage ec2 instances in a given region

## Dependencies
1. boto3
2. dotenv is required in your django project as it will access env variables

## Install
1. install dependencies
2. Add the following to your .env file
    AWS_ACCESS_KEY_ID = ""
    AWS_SECRET_ACCESS_KEY = ""
    
## Usage

```
region = 'ap-south-1'
q2 = qc2(region)
```

### get a list of all instances with relevant details => [{'name': '', 'id': '', 'cpu': {}, 'state': {} }, ...]
```
instances = q2.instances()
```

### get details of 1 instances => return a dict {'name': '', 'id': '', 'cpu': {}, 'state': {} }
```
id = 'i-xxxxxxxxxx'
instance = q2.instance(id)
```

### get state of an instance => returns 'running' | 'stopped' | 
```
id = 'i-xxxxxxxxxx'
instance = q2.state(id)
```

### start an instance => returns True if successful else None
```
id = 'i-xxxxxxxxxx'
instance = q2.start(id)
```

### stop an instance => returns True if successful else None
```
id = 'i-xxxxxxxxxx'
instance = q2.stop(id)
```

