from django.urls import path

from api.views import TriggerFetchYT, VideoView

urlpatterns = [
    path("search/", VideoView.as_view({"get": "list"}), name="videoData-view"),
    path("trigger-fetch-yt/", TriggerFetchYT.as_view(), name="trigger-fetch-yt"),
]
