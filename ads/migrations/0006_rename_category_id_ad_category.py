# Generated by Django 4.1.1 on 2022-09-28 21:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ads", "0005_alter_author_options_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="ad",
            old_name="category_id",
            new_name="category",
        ),
    ]
