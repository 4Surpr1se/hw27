from django.contrib import admin

# Register your models here.
from ads.models import Ad, Categories, Location, Author

admin.site.register(Ad)
admin.site.register(Categories)
admin.site.register(Location)
admin.site.register(Author)
