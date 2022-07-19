from pymemcache.client.base import Client
from threading import Thread
from uuid import uuid4, uuid5
from time import time


class Transcoder:
    def __init__(self, server='127.0.0.1', maximum_workers=1) -> None:
        self.memcached_client = Client(server)
        self.uuid_base = uuid4()
        self.running_workers_count = 0
        self.maximum_workers = maximum_workers
        self.waiting_workers = []

    def transcode_video(self, video, source_file, ctx) -> dict:
        key = str(uuid5(self.uuid_base, f"transcoder_{video.id}"))
        self.memcached_client.set(key, f"{video.id};0;0;{time()};-1", 15)

        thread = Thread(target=self._transcode_content, args=(video.id, source_file, ctx,))

        if self.running_workers_count + 1 > self.maximum_workers:
            self.waiting_workers.append(thread)
        else:
            thread.start()
            self.running_workers_count += 1

        return self.get_transcode_status(video.id)
    
    def _transcode_content(self, id, source_file, ctx):
        pass

    def get_transcode_status(self, video_id: int) -> dict:
        key = str(uuid5(self.uuid_base, f"transcoder_{video_id}"))
        is_working_key = str(uuid5(self.uuid_base, f"transcoder_{video_id}_is_working"))

        video_id, source_progress, om_progress, start_time, current_video_raw = self.memcached_client.get(
            key, f"{video_id};0;0;{time()};-1").split(";")
        is_working = self.memcached_client.get(is_working_key, 'False')
        
        current_video = None
        match (current_video_raw):
            case "0":
                current_video = "source"
            case "1":
                current_video = "om"

        return {
            "video_id": int(video_id),
            "source_progress": float(source_progress),
            "om_progress": float(om_progress),
            "global_progress": int(((float(source_progress) + float(om_progress)) / 2) * 100),
            "start_time": float(start_time),
            "current_video": current_video,
            "is_working": bool(is_working)
        }
