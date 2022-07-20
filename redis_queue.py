from flask_rq2 import RQ
from uuid import uuid4

from models import Video
from database import database

import ffmpeg
import os

redis_queue = RQ()


def _get_video_resolution(filepath) -> tuple:
    try:
        data = ffmpeg.probe(filepath)
    except:
        return None

    if len(data["streams"]) == 0:
        return None

    for stream in data["streams"]:
        if stream["codec_type"] == "video":
            return stream["width"], stream["height"]

    return None


def _max(current_number: int, max_number: int):
    return max_number if current_number > max_number else current_number


def _source_path_gen(extension="mp4"):
    folder = f'static/sources/{uuid4().hex[:2]}/{uuid4().hex[:2]}/'
    os.makedirs(folder, exist_ok=True)

    return folder, f'{uuid4().hex}.{extension}'


def _transcode_mp4(filepath, width: int, height: int):
    mp4_folder, mp4_name = _source_path_gen()
    input_data = ffmpeg.input(filepath)

    video = input_data['v'].filter('scale', width, height)
    audio = None if not input_data.audio else input_data['a']

    (
        ffmpeg
        .output(
            video,
            audio,
            mp4_folder + mp4_name,
            strict=-2,
            **{
                'b:v':'700K',
                'b:a': '96K',
                'c:v': 'libx264',
                'c:a': 'aac'
            }
        )
        .run()
    )

    return mp4_folder + mp4_name


def _transcode_3gp(filepath):
    om_folder, om_name = _source_path_gen("3gp")
    input_data = ffmpeg.input(filepath)

    video = input_data['v'].filter('scale', 176, 144)
    audio = None if not input_data.audio else input_data['a']

    (
        ffmpeg.output(
            video,
            audio,
            om_folder + om_name,
            pix_fmt="yuv420p",
            ar='8000',
            ac='1',
            format="3gp",
            **{'b:v': '60k', 'b:a': '12.20k', 'c:a': 'amr_nb', 'c:v': 'h263'}
        )
        .run()
    )

    return om_folder + om_name


@redis_queue.job("default", "10m")
def transcode(src, video_id):
    video_resolution = _get_video_resolution(src)
    if not video_resolution:
        return

    width = _max(video_resolution[0], 640)
    height = _max(video_resolution[1], 480)

    video = Video.query.get(video_id)

    if not video:
        return

    if not video.mp4_url:
        video.mp4_url = _transcode_mp4(src, width, height)

    if not video.om_url:
        video.om_url = _transcode_3gp(src)

    database.session.commit()
