from django.db import models


class Q3Object(models.Model):
    """
    Stores all S3 objects with tags for easy searchability
    """

    url = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "q3_object"
        verbose_name = "Q3 Object"

    def __str__(self):
        return self.url

    def add_tags(self, tags_dict, override=False):
        if override:
            self.tags_list.all().delete()
        for key, value in tags_dict.items():
            Q3Tag.objects.create(qobject=self, key_name=key, key_value=value)

    def tags(self):
        tagdict = {}
        for tag in self.tags_list.all():
            tagdict[tag.key_name] = tag.key_value
        return tagdict

    @classmethod
    def urls(cls, bucket_name):
        urls = cls.objects.filter(url__startswith=f"s3://{bucket_name}/").values_list(
            "url", flat=True
        )
        return urls


class Q3Tag(models.Model):
    """
    Stores all tags for S3 objects
    """

    qobject = models.ForeignKey(
        Q3Object, on_delete=models.DO_NOTHING, related_name="tags_list"
    )
    key_name = models.CharField(max_length=255)
    key_value = models.CharField(max_length=255)

    class Meta:
        db_table = "q3_tag"
        verbose_name = "Q3 Tag"
        unique_together = ("qobject", "key_name")

    def __str__(self):
        return self.key_name + ":" + self.key_value
