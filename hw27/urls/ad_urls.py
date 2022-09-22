from django.urls import path

from ads.views import AdView, AdDetailView, AdCreateView,\
                      AdDeleteView, AdUpdateView, AdImageAddView\

ad_urlpatterns = [
    path('ad/', AdView.as_view(), name='all_ads'),
    path("ad/<int:pk>/", AdDetailView.as_view(), name='ad_by_id'),
    path('ad/create/', AdCreateView.as_view(), name='create_ad'),
    path("ad/<int:pk>/delete/", AdDeleteView.as_view(), name='ad_delete_by_id'),
    path("ad/<int:pk>/update/", AdUpdateView.as_view(), name='ad_update_by_id'),
    path("ad/<int:pk>/upload_image/", AdImageAddView.as_view(), name='ad_image_upload'),
]
