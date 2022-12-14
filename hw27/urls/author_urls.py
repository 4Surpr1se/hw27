from django.urls import path
from ads.views import AuthorView, AuthorDetailView,\
                      AuthorDeleteView, AuthorUpdateView

from ads.views.author_views import AuthorAPICreate

author_urlpatterns = [
    path('author/', AuthorView.as_view(), name='all_ads'),
    path('author/create/', AuthorAPICreate.as_view(), name='create_author'),
    path("author/<int:pk>/", AuthorDetailView.as_view(), name='author_by_id'),
    path("author/<int:pk>/delete/", AuthorDeleteView.as_view(), name='author_delete_by_id'),
    path("author/<int:pk>/update/", AuthorUpdateView.as_view(), name='author_update_by_id')
]
