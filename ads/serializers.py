from rest_framework import serializers

from ads.models import User, Location, Ad


# TODO Вынести сериализаторы в отдельный файл
from ads.models.selection import Selection


class AlbumSerializer(serializers.ModelSerializer):
    # location_id = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='id'
    #     )
    # TODO ВЕРНУТЬ GEOHELPER И ВОЗВРАЩАТЬ ПОЛЕ NAME У LOCATION

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = super().create(validated_data)

        user.set_password(validated_data['password'])
        user.save()

        return user


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class SelectionSerializer(serializers.ModelSerializer):
    items = AdSerializer(read_only=True, many=True)

    class Meta:
        model = Selection
        fields = '__all__'

