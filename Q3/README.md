# Q3 - A Qux module for AWS S3

## Dependencies
1. s3fs
2. pandas
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
### Upload File => returns True if success else None
```
fileurl = "s3://enine-test/mapping.csv"
filepath = "/Users/psathaye/Downloads/mapping.csv"
q3.upload_file(fileurl, filepath)
```

### Upload Dataframe => returns True if success else None
```
fileurl = "S3://enine-test/mapping.csv"
q3.upload_fileobj(fileurl, df)
```

### List Files => list of files : ['filename1', 'filename2', ...]
```
bucket_name = "enine-test"
filelist = q3.list(bucket_name, prefix="2022/01/")

all_filelist = q3.list(bucket_name)
```

### File Exists => check if file exists returns True or False
```
fileurl = "s3://enine-test/mapping.csv"
q.exists(fileurl)
```

### Download dataframe => returns dataframe for an S3 fileurl if success or None
```
fileurl = "s3://enine-test/mapping.csv"
df = q.download_df(fileurl)
```

### Download file => returns file for an S3 fileurl if success or None
```
fileurl = "s3://enine-test/mapping.csv"
df = q.download_file(fileurl)
```

### Add Tags => returns True if success else None. Tags are all strings.
```
fileurl = "s3://enine-test/mapping.csv"
tags = {"report_name" : "settlement_report", "report_id" : "1234"}
put_tags(fileurl, tags, override=True) => will delete all previous tags and then add
put_tags(fileurl, tags, override=False) => will add new tags
```

### get tags for a fileurl => returns a dict
```
fileurl = "s3://enine-test/mapping.csv"
tags = q.get_tags(fileurl)
```
