import os

from celery import shared_task

from api.services.sync.video import VideoSync


@shared_task
def fetch_yt():
    VideoSync().syncRecordsFromYT()

    return True
