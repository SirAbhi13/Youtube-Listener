from django.urls import path

from api.views import VideoView

urlpatterns = [
    path("search/", VideoView.as_view({"get": "list"}), name="videoData-view")
]
