# Q3 - A Qux module for AWS S3

## Dependencies
1. boto3
2. pandas
2. dotenv is required in your django project as it will access env variables

## Install
1. install dependencies
```
pip install pandas
pip install boto3
```
2. Add the following to your .env file
    AWS_S3_ACCESS_KEY_ID = ""
    AWS_S3_SECRET_ACCESS_KEY = ""

## Usage

```

from QWS import Q3

q3_obj = Q3()

```
### List buckets => returns a list of buckets ['test1', 'test2', ...]
```
buckets = qm.list_buckets()
```

### List Files => list of files : ['filename1', 'filename2', ...]
```
bucket_name = "enine-test"
filelist = q3.list(bucket_name, prefix="2022/01/")

all_filelist = q3.list(bucket_name)
```

### Download dataframe => returns dataframe for an S3 fileurl if success or None
```
bucket_name = 'enine-test'
filename = 'mapping.csv'

df = q.download_df(bucket_name, filename)
```

### Download file => returns file from S3 if success or None
```
bucket_name = 'enine-test'
filename = 'mapping.csv'

file = q.download_file(bucket_name, filename)
```

### Upload File => returns True if success else None
```
bucket_name = 'enine-test'
filename = 'mapping.csv'
filepath = "/Users/psathaye/Downloads/mapping.csv"
q3.upload_file(bucket_name, filename, filepath)
```

### Upload FileObject => returns True if success else None
```
bucket_name = 'enine-test'
df = pd.read_csv('mapping.csv')
df.read_csv(buffer)
q3.upload_fileobj(bucket_name, filename, buffer)
```

### Upload Dataframe => returns True if success else None
```
bucket_name = 'enine-test'
df = pd.read_csv("/Users/psathaye/Downloads/mapping.csv")
q3.upload_df(bucket_name, filename, df)
```

### Add Tags => returns True if success else None. Tags are all strings.
```
tags = {"report_name" : "settlement_report", "report_id" : "1234"}
bucket_name = 'enine-test'
filename = 'mapping.csv'

put_tags(bucket_name, filename, tags, overwrite=True) => will delete all previous tags and then add

put_tags(bucket_name, filename, tags, overwrite=False) => will add new tags
```

### get tags for a file => returns a dict
```
bucket_name = 'enine-test'
filename = 'mapping.csv'
tags = q.get_tags(bucket_name, filename)
```

### get list page iterator => return a page iterator for getting a list of objects for a given bucket
```
bucket_name = 'enine-test'
prefix = '2022/01'
pagesize = 1000
page_iterator = q.get_list_page_iterator(bucket_name, prefix, pagesize)
for page in page_iterator:
    print(page["Contents"])
```