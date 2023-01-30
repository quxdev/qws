from .models import Q3Object
from q3.services import Q3


class Q3Managed(object):
    def __init__(self):
        self.q = Q3()

    def upload_file(self, fileurl, filepath, tags_dict={}):
        done = self.q.upload_file(fileurl, filepath)
        if done:
            if self.q.put_tags(fileurl, tags_dict):
                qo = Q3Object.objects.create(url=fileurl)
                qo.add_tags(tags_dict)
                return True
        return None

    def upload_df(self, fileurl, df, tags_dict={}):
        done = self.q.upload_df(fileurl, df)
        if done:
            if self.q.put_tags(fileurl, tags_dict):
                qo = Q3Object.objects.create(url=fileurl)
                qo.add_tags(tags_dict)
                return True
        return None

    def download_df(self, fileurl):
        return self.q.download_df(fileurl)

    def download_file(self, fileurl):
        return self.q.download_file(fileurl)

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
        if self.q.put_tags(fileurl, tags_dict, override):
            qo = Q3Object.objects.get(url=fileurl)
            qo.add_tags(tags_dict)
            return True
        return None

    def get_tags(self, fileurl):
        return self.q.get_tags(fileurl)

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
            qobj = Q3Object.objects.create(url=url)
            count = count + 1
            tags = self.q.get_tags(url)
            if tags and qobj:
                qobj.add_tags(tags)
        print(f"Synced {count} objects")
        return True

    def bulk_tag_upload(self, df):
        count = 0
        for index, row in df.iterrows():
            t = {}
            for col in [x for x in df.columns if x != "url"]:
                t[col] = str(row[col]) if col != "url" else None
            if self.q.put_tags(row["url"], t, override=True):
                qo, created = Q3Object.objects.get_or_create(url=row["url"])
                qo.add_tags(t, override=True)
                count = count + 1
        print(f"Added tags to {count} url objects")
        return True
