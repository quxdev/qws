# q3min.py - A Simple Qux module for AWS S3

## Dependencies
1. import boto3
2. from io import BytesIO
3. import gzip
4. from dataclasses import dataclass

## Install
1. install dependencies
```
pip install boto3
```
## Usage

### import
```
from QWS.q3.q3min  import S3config, S3path, Q3
```

### Config - access_key and secret_key are optional, if not passed the default config will be used
```
# create an aws config for accessing S3
access_key = ""
secret_key = ""
config = S3config(access_key, secret_key)

# You can pass additional parameters to config for enabling cache and providing a cache directory
# The cache directory should exist and will not be created by QWS
cache_active = True
cache_dir = "data/cache"
config = S3config(access_key, secret_key, cache_active, cache_dir)

#User the following to check if cache is enabled
config.cache_enabled   => returns True or False

```
### create S3Path
```
path = "s3://enine-test/parag/test.csv"
spath = S3Path(path)
or 
bucket = "enine-test"
key = "parag/test.csv"
spath = S3Path(bucket, key)

s3path.path => returns "s3://enine-test/parag.csv"
s3path.bucket => returns "enine-test"
s3path.key => returns "parag/test.csv"
s3path.is_gzip => returns False
s3path.is_zip => returns False
```

### Q3 object for uploading and downloading S3 files
```
q3 = Q3(config) # use the config object created earlier

spath = S3path("s3://enine-test/parag/test.csv")
```

#### list files in a bucket for a given s3path => returns a list of s3path objects
```
paths = q3.list(s3path)
for p in path:
    print(p.path, p.bucket, p.key)
```

#### check if file exists in S3
```
q3.exists(s3path) => returns True if file exists on s3 else False
```

#### download file - will automatically uncompress .gz files
```
fileobj = q3.download(s3path) => return BytesIO
df = pd.read_csv(fileobj)
```

#### upload file - will automatically compress if extension in path is .gz
```
path = "/downloads/test.csv"
buffer = BytesIO()
pd.read_csv(path).to_csv(buffer)
spath = S3path("enine-test", "parag/test.csv.gz")
q3.upload(spath, buffer) => returns True if successful

```

## New Methods for cache and zip support

#### check if file exists in cache

```
q3.exists_in_cache(s3path) => returns True if file exists on s3 else False
```

#### list files in cache for a given s3path => returns a list of cached files
```
filelist = q3.list_cache(s3path)
for f in filelist:
    print(f)   => full path of the file
```

#### download file with cache first strategy: 
#### cache first strategy: Will return file from cache if found, else fetch from s3, save in cache and return
```
results = q3.download_v2(s3path) => return BytesIO
# results = [{"filename": <filename>, "fileobj": <bytesIO buffer>, "from": "cache|s3", "source": <full path>"}, ...]
for r in results:
    df = pd.read_csv(r["fileobj"])
    print(r["filename"], r["from"], r["source"])
    print(df)
```

#### Upload file with cache first strategy
This will store the file to cache after successful upload to S3
```
path = "/downloads/test.csv"
buffer = BytesIO()
pd.read_csv(path).to_csv(buffer)
spath = S3path("enine-test", "parag/test.csv.gz")
q3.upload_v2(spath, buffer) => returns True if successful

```
