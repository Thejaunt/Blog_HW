# Generated by Django 4.2.3 on 2023-07-29 23:12

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0005_alter_comment_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="post",
            options={"ordering": ("-created_at",)},
        ),
    ]
