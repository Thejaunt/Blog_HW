# Generated by Django 4.2.3 on 2023-07-29 23:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0004_alter_comment_options_alter_post_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={"ordering": ("-created_at",)},
        ),
    ]
