from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Video
from api.serializers import VideoRequestSerializer, VideoSerializer
from api.tasks import fetch_yt


class VideoView(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    queryset = Video.objects.all()

    def get_queryset(self):
        """
        List all task history for all accounts
        or for specific account id/s.
        """
        serializer = VideoRequestSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        channel_id = serializer.validated_data.get("channel_id")
        video_id = serializer.validated_data.get("video_id")
        channel_title = serializer.validated_data.get("channel_title")
        from_date = serializer.validated_data.get("from_date")
        to_date = serializer.validated_data.get("to_date")
        print(serializer.validated_data, "hihohi")
        query = Q()
        if channel_id:
            query &= Q(channel_id=channel_id)
        if video_id:
            query &= Q(video_id=video_id)
        if channel_title:
            query &= Q(channel_title__icontains=channel_title)
        if from_date:
            query &= Q(published_at__gte=from_date)
        if to_date:
            query &= Q(published_at__lte=to_date)

        return Video.objects.filter(query)


class TriggerFetchYT(APIView):

    def post(self, request, format=None):
        fetch_yt.delay()
        return Response({"status": "Task added to queue"})
