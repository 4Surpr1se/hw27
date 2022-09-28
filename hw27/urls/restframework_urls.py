from django.urls import include, path

framework_urlpatterns = [
    path('api-auth/', include('rest_framework.urls'))
]