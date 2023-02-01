from .models import Q3Object
from ..q3.shared import Q3


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

    def find(self, prefix="", tags_dict={}):
        queryset = Q3Object.objects.filter(url__startswith=prefix)
        for key, value in tags_dict.items():
            queryset = queryset.filter(
                tags_list__key_name=key, tags_list__key_value=value
            )

        return [{"url": x.url, "tags": x.tags()} for x in queryset]

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

    def missing_s3(self, bucket_name):
        urls = Q3Object.urls(bucket_name)
        s3urls = self.q.list(bucket_name)
        missing = list(set(urls).difference(set(s3urls)))
        return missing

    def sync(self, bucket_name):
        urls = Q3Object.urls(bucket_name)
        s3urls = self.q.list(bucket_name)
        missing = set(s3urls).difference(set(urls))
        count = 0
        for url in missing:
            url_bucket, url_filename = self.split_fileurl(url)

            qobj = Q3Object.objects.create(url=url)
            count = count + 1
            tags = self.q.get_tags(url_bucket, url_filename)
            if tags and qobj:
                qobj.add_tags(tags)
        print(f"Synced {count} objects")
        return True

    def bulk_tag_upload(self, df, overwrite=True):
        count = 0
        for index, row in df.iterrows():
            t = {}
            for col in [x for x in df.columns if x != "url"]:
                t[col] = str(row[col]) if col != "url" else None

            bucket_name, filename = self.split_fileurl(row["url"])

            if self.q.put_tags(bucket_name, filename, t, overwrite):
                qo, created = Q3Object.objects.get_or_create(url=row["url"])
                qo.add_tags(t, overwrite)
                count = count + 1
        print(f"Added tags to {count} url objects")
        return True
