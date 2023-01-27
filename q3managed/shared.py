from .models import Q3Object, Q3Tag
from q3.services import Q3


class Q3Managed(Q3):
    def __init__(self):
        q = Q3()

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

    def get_df(self, fileurl):
        return self.q.get_df(fileurl)

    def get_file(self, fileurl):
        return self.q.get_file(fileurl)

    def exists(self, fileurl):
        return Q3Object.objects.filter(url=fileurl).exists()

    def find(self, prefix, tags_dict={}):
        queryset = Q3Object.objects.filter(url__startswith=prefix)
        for key, value in tags_dict.items():
            queryset = queryset.filter(tags__key_name=key, tags__key_value=value)

        return [{"url": x.url, "tags": x.tags.all()} for x in queryset]

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
        urls = Q3Object.objects.filter(
            url__startswith=f"s3://{bucket_name}/"
        ).values_list("url", flat=True)
        s3urls = self.q.list(bucket_name)
        missing = set(urls).difference(set(s3urls))
        return missing

    def sync(self, bucket_name):
        urls = Q3Object.objects.filter(
            url__startswith=f"s3://{bucket_name}/"
        ).values_list("url", flat=True)
        s3urls = self.q.list(bucket_name)
        missing = set(s3urls).difference(set(urls))
        return missing

    def bulk_tag_upload(self, df):
        for index, row in df.iterrows():
            for col in df.columns:
                t = {"key_name": col, "key_value": row[col]}
                if self.q.put_tags(row["url"], t, override=False):
                    qo = Q3Object.objects.get_or_create(url=row["url"])
                    qo.add_tags(row["url"], row["tags"], override=True)
                    return True
        return None
