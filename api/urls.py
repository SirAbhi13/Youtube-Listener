from django.urls import path

from .views import VideoDataView

urlpatterns = [path("searchyt/", VideoDataView.as_view(), name="videoData-view")]
