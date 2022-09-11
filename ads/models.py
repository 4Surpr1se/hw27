from django.db import models


class Ad(models.Model):
    Id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='')
    author = models.CharField(max_length=100, default='')
    price = models.PositiveSmallIntegerField(null=True, blank=True)
    description = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=100, default='')
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name
