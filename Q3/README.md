# Q3 - A Qux module for AWS S3

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

from QWS import Q3

q3_obj = Q3()

```
### List buckets => returns a list of bucket names ['bucket-1', 'bucket-2']
```
q3.list_buckets()
```

### Upload File => returns True if success else None
```
q3.upload_file(bucket_name, filename, path)
```

### Upload File Object (binary) => returns True if success else None
```
q3.upload_fileobj(bucket_name, filename, data)
```

### List Files => list of dict [{'key': 'xyz', 'last_modified' : timestamp}, ...]
```
filelist = q3.list(bucket_name, prefix="2022/01/")

all_filelist = q3.list(bucket_name)
```


