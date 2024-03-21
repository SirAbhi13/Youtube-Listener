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
            "q": "cricket",
            "publishedAfter": "2024-03-21T16:28:35Z",
            "type": "video",
            "key": self.api_key,
            "maxResults": 50,
            "order": "date",
        }

    def syncRecordsFromYT(self):
        try:
            response = requests.get(f"https://{self.url}", params=self.request_body)
            response.raise_for_status()
            response = response.json()
            request_count = 1
            logger.info("Fetched first page")

            video_items = response.get("items")
            pageToken = response.get("nextPageToken")
            while pageToken and request_count < 3:
                self.request_body["pageToken"] = pageToken
                response = (
                    requests.get(f"https://{self.url}", params=self.request_body)
                ).json()
                video_items.extend(response.get("items"))
                pageToken = response.get("nextPageToken")
                request_count += 1

            logger.info(
                f"syncing data from yt successful, {request_count} requests made."
            )

            logger.info(f"fetched {len(video_items)} records")
            self.syncRecordsToDB(video_items)
        except Exception as e:
            logger.error(f"Error in fetching data from youtube. {e}")

    def syncRecordsToDB(self, video_items):

        try:
            logger.info("syncing records in batch of 10,000")
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
            logger.info(f"inserting {len(video_instances)} records.")
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
            logger.info("syncing data to db successful")
        except Exception as e:
            logger.error(f"Error in syncing data to database, {e}")
