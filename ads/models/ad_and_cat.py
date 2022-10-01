from django.db import models

from ads.models.loc_and_user import User


class Categories(models.Model):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name


class Ad(models.Model):

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.PositiveSmallIntegerField(null=True, blank=True)
    description = models.TextField(default='')
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
