# Generated by Django 4.2.3 on 2023-07-30 20:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0006_alter_post_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="is_published",
            field=models.BooleanField(default=True),
        ),
    ]