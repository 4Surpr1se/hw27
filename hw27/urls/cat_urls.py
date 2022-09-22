from django.urls import path
from ads.views import CatView, CatDetailView, CatCreateView,\
                      CatDeleteView, CatUpdateView

cat_urlpatterns = [
    path('cat/', CatView.as_view(), name='all_cats'),
    path("cat/<int:pk>/", CatDetailView.as_view(), name='cat_by_id'),
    path('cat/create/', CatCreateView.as_view(), name='create_cat'),
    path("cat/<int:pk>/delete/", CatDeleteView.as_view(), name='cat_delete_by_id'),
    path("cat/<int:pk>/update/", CatUpdateView.as_view(), name='cat_update_by_id'),
]
