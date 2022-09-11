from django.db import models


class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name
