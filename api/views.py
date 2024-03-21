from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import VideoData
from .serializers import VideoDataSerializer


class VideoDataView(APIView):

    def get(self):
        pass

    pass
