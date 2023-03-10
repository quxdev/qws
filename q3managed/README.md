# q3managed: Wrapper for a managed S3 module that maintains meta data in DB for easy search and access on Tags and Prefix both. It uses the q3 module internally.

## Dependencies
```
django - for the data models
q3 - for accessing S3
```
## Install dependencies and create database models
```
pip install s3fs
pip install pandas

python manage.py migrate qws 

Add the following to your .env file
    AWS_S3_ACCESS_KEY_ID = ""
    AWS_S3_SECRET_ACCESS_KEY = ""
```

## Usage
```
q3m = Q3Managed()
```

### Upload File with tags => returns True if success else None
```
fileurl = "s3://enine-test/mapping.csv"
tags_dict = {'report_name': 'test', 'report_id': 1}
filepath = "/Users/psathaye/Downloads/mapping.csv"
status = q3m.upload_file(fileurl, filepath, tags_dict)
```

### Upload DF with tags => returns True if success else None
```
fileurl = "s3://enine-test/mapping.csv"
tags_dict = {'report_name': 'test', 'report_id': 1}
filepath = "/Users/psathaye/Downloads/mapping.csv"
df = pd.read_csv(filepath)
status = q3m.upload_file(fileurl, df, tags_dict)
```

### Download DF => returns dataframe if success else None. Will convert zip file to a dataframe as well.
```
fileurl = "s3://enine-test/mapping.csv"
df = q3m.download_df(fileurl)
```

### Download File => returns file like object if success else None
```
fileurl = "s3://enine-test/mapping.csv"
fileobj = q3m.download_df(fileurl)
```

### Check if fileurl exists => returns true or false
```
fileurl = "s3://enine-test/mapping.csv"
df = q3m.exists(fileurl)
```

### Find Files => returns a list of dict [{'url' : 's3://enine-test/mapping.csv', 'report_name': 'test'}]
```
prefix = "s3://enine-test"
tags = {'report_id' : '1'}
filelist = q3m.find(prefix, tags)
```

### Add Tags to existing files => returns True if success else None. Override existing tags or add new using the override param.
```
fileurl = "s3://enine-test/mapping.csv"
tags_dict = {'report_name': 'test', 'report_id': 1}
df = q3m.add_tags(fileurl, tags_dict, override=False)
```

### Get Tags for existing file => returns a dict of tags {'report_name': 'test', 'report_id' : 1} 
```
fileurl = "s3://enine-test/mapping.csv"
tags = q3m.get_tags(fileurl)
```

### Find Files with no tags => returns a list of file urls
```
prefix = "s3://enine-test"
filelist = q3m.find_missingtags(prefix)
```

### Sync files from S3 to the data model - will add tags if found => returns True or None
```
bucket_name = "enine-test"
status = q3m.sync(bucket_name)
```

### Bulk Tag upload => takes a data frame with columns [url, 'tagname1', 'tagname2', ...]. Returns True or None.
```
path = "Users/psathaye/Downloads/tagfile"
status = q3m.bulk_tag_upload(path, overwrite=False)
```

### Move => move an S3 object returns True or None
```
from_url = "s3://enine-test/2022/testzip.zip"
to_url = "s3://enine-test/2023/testzip.zip"

q3m.move(from_url, to_url)
```
### Download multiple files as df from S3. Downloads files in parallel for fast processing.
```
results = []
files = qm.find("s3://enine-test/test")
for key, result in qm.download_df_multiple(files):
    print(f"Downloaded {key}")
    results.append(result)
df = pd.concat(results)
print(f"Downloaded {len(results)} files")
return df