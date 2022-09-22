from django.urls import path

from ads.views import IndexView

index_urlpatterns = [
    path('', IndexView.as_view(), name='index')
]
