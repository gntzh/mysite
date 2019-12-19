from utils.rest.serializers import drf as serializers

from ..models import Album, ThirdPartyImage, Hosting


class TPImageSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ThirdPartyImage
        fields = '__all__'
        extra_kwargs = {}


class HostingSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Hosting
        fields = '__all__'
        extra_kwargs = {}


class AlbumSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Album
        fields = '__all__'
        extra_kwargs = {}
