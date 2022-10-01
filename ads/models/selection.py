from django.db import models

from ads.models import User, Ad


class Selection(models.Model):
    items = models.ManyToManyField(Ad)
    name = models.CharField(max_length=30, default='')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
