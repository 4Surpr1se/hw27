from .ad_urls import ad_urlpatterns
from .cat_urls import cat_urlpatterns
from .author_urls import author_urlpatterns
from .admin_url import admin_urlpatterns
from .index_url import index_urlpatterns

from django.conf.urls.static import static

from hw27 import settings

urlpatterns = ad_urlpatterns + cat_urlpatterns +\
              author_urlpatterns + admin_urlpatterns\
              + index_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
