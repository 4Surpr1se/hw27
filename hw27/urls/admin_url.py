from django.contrib import admin
from django.urls import path

from ads.views import IndexView

admin_urlpatterns = [
    path('admin/', admin.site.urls)
]
