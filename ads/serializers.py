from rest_framework import serializers

from ads.models import Author, Location


# TODO Вынести сериализаторы в отдельный файл


class AlbumSerializer(serializers.ModelSerializer):
    # location_id = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='id'
    #     )
    # TODO ВЕРНУТЬ GEOHELPER И ВОЗВРАЩАТЬ ПОЛЕ NAME У LOCATION

    class Meta:
        model = Author
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
