# Generated by Django 4.2.3 on 2023-07-27 04:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="is_published",
            field=models.BooleanField(default=False),
        ),
    ]
