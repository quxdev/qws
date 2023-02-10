from .models import Q3Object
from ..q3.shared import Q3
import os
import pandas as pd
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor


class Q3Managed(object):
    def __init__(self):
        self.q = Q3()

    # returns bucket_name and key
    def split_fileurl(self, fileurl):
        l = fileurl.replace("s3://", "").split("/")
        if len(l) < 2:
            return None, None
        return l[0], "/".join(l[1:])

    def upload_file(self, fileurl, filepath, tags_dict={}):
        bucket_name, filename = self.split_fileurl(fileurl)
        if bucket_name is None or filename is None:
            return None

        done = self.q.upload_file(bucket_name, filename, filepath)
        if done:
            if self.q.put_tags(bucket_name, filename, tags_dict):
                qo = Q3Object.objects.create(url=fileurl)
                qo.add_tags(tags_dict)
                return True
        return None

    def upload_df(self, fileurl, df, tags_dict={}):
        bucket_name, filename = self.split_fileurl(fileurl)
        if bucket_name is None or filename is None:
            return None

        done = self.q.upload_df(bucket_name, filename, df)
        if done:
            if self.q.put_tags(bucket_name, filename, tags_dict):
                qo = Q3Object.objects.create(url=fileurl)
                qo.add_tags(tags_dict)
                return True
        return None

    def download_df(self, fileurl):
        bucket_name, filename = self.split_fileurl(fileurl)
        if bucket_name is None or filename is None:
            return None

        return self.q.download_df(bucket_name, filename)

    def download_file(self, fileurl):
        bucket_name, filename = self.split_fileurl(fileurl)
        if bucket_name is None or filename is None:
            return None

        return self.q.download_file(bucket_name, filename)

    def exists(self, fileurl):
        return Q3Object.objects.filter(url=fileurl).exists()

    def find(self, prefix="", tags_dict={}, limit=1000):
        queryset = Q3Object.objects.filter(url__startswith=prefix)
        for key, value in tags_dict.items():
            queryset = queryset.filter(
                tags_list__key_name=key, tags_list__key_value=value
            )

        return [{"url": x.url, "tags": x.tags()} for x in queryset[:limit]]

    def find_missingtags(self, prefix):
        queryset = Q3Object.objects.filter(url__startswith=prefix)
        queryset = queryset.filter(tags=None)

        return queryset.values_list("url", flat=True)

    def add_tags(self, fileurl, tags_dict, override=False):
        bucket_name, filename = self.split_fileurl(fileurl)
        if bucket_name is None or filename is None:
            return None

        if self.q.put_tags(bucket_name, filename, tags_dict, override):
            qo = Q3Object.objects.get(url=fileurl)
            qo.add_tags(tags_dict, override)
            return True
        return None

    def get_tags(self, fileurl):
        bucket_name, filename = self.split_fileurl(fileurl)
        if bucket_name is None or filename is None:
            return None

        return self.q.get_tags(bucket_name, filename)

    # add S3 objects that are missing in the model
    def sync(self, bucket_name):
        count = 0
        page_iterator = self.q.get_list_page_iterator(bucket_name)
        for page in page_iterator:
            urllist = ["s3://" + bucket_name + "/" + x["Key"] for x in page["Contents"]]
            objurls = Q3Object.objects.filter(url__in=urllist).values_list(
                "url", flat=True
            )
            missing = list(set(urllist).difference(set(objurls)))
            count = count + self.add_object(missing)
        print(f"Synced Total {count} objects")

    def add_object(self, urllist):
        count = 0
        for url in urllist:
            url_bucket, url_filename = self.split_fileurl(url)
            qobj = Q3Object.objects.create(url=url)
            count = count + 1
            tags = self.q.get_tags(url_bucket, url_filename)
            if tags and qobj:
                qobj.add_tags(tags)
        print(f"added {count} objects")
        return count

    def bulk_tag_upload(self, path, overwrite=True):
        if not os.path.exists(path):
            return False

        with pd.read_csv(path, chunksize=1000) as reader:
            for df in reader:
                self.upload_tags(df, overwrite)

    def upload_tags(self, df, overwrite=True):
        count = 0
        for index, row in df.iterrows():
            t = {}
            for col in [x for x in df.columns if x != "url"]:
                t[col] = str(row[col])

            bucket_name, filename = self.split_fileurl(row["url"])

            if self.q.put_tags(bucket_name, filename, t, overwrite):
                qo, created = Q3Object.objects.get_or_create(url=row["url"])
                qo.add_tags(t, overwrite)
                count = count + 1
        print(f"Added tags to {count} url objects")
        return True

    def move(self, from_url, to_url):
        if from_url == to_url:
            return None

        old_bucket, from_prefix = self.split_fileurl(from_url)
        new_bucket, to_prefix = self.split_fileurl(to_url)

        qo = Q3Object.objects.get(url=from_url)
        if qo:
            if self.q.move(old_bucket, from_prefix, new_bucket, to_prefix):
                qo.url = qo.url = to_url
                qo.save()
                print(f"Updated {from_prefix} to {to_prefix} objects")
                return True
        return None

    def download_df_multiple(self, files):
        with ThreadPoolExecutor(max_workers=8) as executor:
            future_to_key = {
                executor.submit(self.download_df, file): file for file in files
            }

            for future in futures.as_completed(future_to_key):
                key = future_to_key[future]
                exception = future.exception()

                if not exception:
                    yield key, future.result()
                else:
                    yield key, exception
