# Generated by Django 4.1.1 on 2022-09-22 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ads", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ad",
            name="address",
        ),
    ]