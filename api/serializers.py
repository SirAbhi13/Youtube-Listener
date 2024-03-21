from datetime import datetime, timedelta

from django.utils import timezone
from rest_framework import serializers

from api.models import Video


class EpochDateTimeField(serializers.Field):
    def __init__(self, *args, **kwargs):
        default_value = kwargs.pop("default", None)
        super().__init__(*args, default=default_value, **kwargs)

    def to_representation(self, value):
        return int(value.timestamp())

    def to_internal_value(self, data):
        return datetime.fromtimestamp(int(data), tz=timezone.get_default_timezone())


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"


class VideoRequestSerializer(serializers.Serializer):

    channel_id = serializers.CharField(max_length=255, required=False)
    video_id = serializers.CharField(max_length=50, required=False)
    channel_title = serializers.CharField(max_length=255, required=False)

    from_date = EpochDateTimeField(
        required=False,
    )

    to_date = EpochDateTimeField(
        required=False,
    )
