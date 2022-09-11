# Generated by Django 4.1.1 on 2022-09-10 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=100)),
                ('author', models.CharField(default='', max_length=100)),
                ('price', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('description', models.CharField(default='', max_length=100)),
                ('address', models.CharField(default='', max_length=100)),
                ('is_published', models.BooleanField(default=False)),
            ],
        ),
    ]