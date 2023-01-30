# q3managed: Wrapper for a managed S3 module that maintains meta data in DB for easy search and access on Tags and Prefix both. It uses the q3 module internally.

## Dependencies
```
django - for the data models
q3 - for accessing S3
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

### Download DF => returns dataframe if success else None
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
fileurl = "s3://enine-test/mapping.csv"
filelist = q3m.download_df(fileurl)
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

### Find Files that are in the meta data model but not on S3 => returns a list of file urls
```
bucket_name = "enine-test"
filelist = q3m.missing_s3(bucket_name)
```

### Sync files from S3 to the data model - will add tags if found => returns True or None
```
bucket_name = "enine-test"
status = q3m.sync(bucket_name)
```

### Bulk Tag upload => takes a data frame with columns [url, 'tagname1', 'tagname2', ...]. Returns True or None.
```
df = pd.read_csv("Users/psathaye/Downloads/tagfile")
status = q3m.bulk_tag_upload(df)
```