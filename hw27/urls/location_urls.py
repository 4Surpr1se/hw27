from rest_framework import routers

from ads.views import LocationViewSet

router = routers.SimpleRouter()
router.register('location', LocationViewSet)

location_urlpatterns = router.urls

