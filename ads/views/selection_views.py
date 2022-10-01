from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import Selection
from ads.permissions import SelectionPermission
from ads.serializers import SelectionSerializer

# TODO Пагинацию


class SelectionViewSet(ModelViewSet):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated, SelectionPermission]
