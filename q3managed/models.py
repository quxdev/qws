from django.db import models


class Q3Object(models.Model):
    """
    Stores all S3 objects with tags for easy searchability
    """

    url = models.CharField(max_length=255, unique=True)

    class Meta:
        table_name = "q3_object"
        verbose_name = "Q3 Object"

    def __str__(self):
        return self.url

    def add_tags(self, tags_dict):
        for key, value in tags_dict.items():
            Q3Tag.objects.create(qobject=self, key_name=key, key_value=value)


class Q3Tag(models.Model):
    """
    Stores all tags for S3 objects
    """

    qobject = models.ForeignKey(
        Q3Object, on_delete=models.DO_NOTHING, related_name="tags"
    )
    key_name = models.CharField(max_length=255)
    key_value = models.CharField(max_length=255)

    class Meta:
        table_name = "q3_tag"
        verbose_name = "Q3 Tag"
        unique_together = ("qobject", "key_name")

    def __str__(self):
        return self.key_name + ":" + self.key_value
