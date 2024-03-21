from datetime import datetime
from logging import getLogger

import requests
from dateutil import parser

from api.constants import YOUTUBE_API_URL
from api.models import Video
from yt_listener.settings import YOUTUBE_API_KEY

logger = getLogger(__name__)


class VideoSync:
    def __init__(self):
        self.url = YOUTUBE_API_URL
        self.api_key = YOUTUBE_API_KEY
        self.request_body = {
            "part": "snippet",
            "type": "video",
            "key": self.api_key,
            "maxResults": 50,
            "order": "date",
        }

    def syncRecordsFromYT(self):

        try:
            response = (requests.get(self.url, params=self.request_body)).json()
            video_items = response.get("items")
            nextPageToken = response.get("nextPageToken")
            while nextPageToken:
                response = (requests.get(self.url, params=self.request_body)).json()
                video_items.append(response.get("items"))
                nextPageToken = response.get("nextPageToken")
        except:
            logger.error("Error in fetching data from youtube")

        self.sycnRecordsToDB(video_items)

    def syncRecordsToDB(self, video_items):

        try:
            video_instances = []
            for video in video_items:

                video_instances.append(
                    Video(
                        title=video.get("snippet").get("title"),
                        description=video.get("snippet").get("description"),
                        video_id=video.get("id").get("videoId"),
                        channel_id=video.get("snippet").get("channelId"),
                        published_at=parser.parse(
                            video.get("snippet").get("publishedAt")
                        ),
                        thumbnail_url=video.get("snippet")
                        .get("thumbnails")
                        .get("medium")
                        .get("url"),
                        channel_title=video.get("snippet").get("channelTitle"),
                    )
                )
            Video.objects.bulk_create(
                video_instances,
                batch_size=10000,
                update_conflicts=True,
                update_fields=[
                    "title",
                    "description",
                    "thumbnail_url",
                    "channel_title",
                ],
                unique_fields=["video_id", "channel_id"],
            )
        except:
            logger.error("Error in syncing data to database")
