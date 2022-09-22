from django.db import models


class Location(models.Model):

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    name = models.CharField(max_length=100, default='')
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.name


class Author(models.Model):
    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['username']

    ROLES = [('member', 'member'),
             ('moderator', 'moderator'),
             ('admin', 'admin')]

    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    username = models.CharField(max_length=100, default='')
    password = models.CharField(max_length=100, default='')
    role = models.CharField(max_length=10, choices=ROLES)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.username
