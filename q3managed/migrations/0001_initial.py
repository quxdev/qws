# Generated by Django 4.1.5 on 2023-01-27 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Q3Object",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("url", models.CharField(max_length=255, unique=True)),
            ],
            options={
                "verbose_name": "Q3 Object",
                "db_table": "q3_object",
            },
        ),
        migrations.CreateModel(
            name="Q3Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("key_name", models.CharField(max_length=255)),
                ("key_value", models.CharField(max_length=255)),
                (
                    "qobject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="tags",
                        to="q3managed.q3object",
                    ),
                ),
            ],
            options={
                "verbose_name": "Q3 Tag",
                "db_table": "q3_tag",
                "unique_together": {("qobject", "key_name")},
            },
        ),
    ]
