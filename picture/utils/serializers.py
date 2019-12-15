from utils.rest.serializers import drf as serializers

from .. import models


class TPImageSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.ThirdPartyImage
        fields = '__all__'
        extra_kwargs = {}


class HostingSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Hosting
        fields = '__all__'
        extra_kwargs = {}


class AlbumSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Album
        fields = '__all__'
        extra_kwargs = {}
