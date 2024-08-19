import enum


class Queue(enum.StrEnum):
    PRE_YOUTUBE = "pre_youtube"
    DOWNLOAD_YOUTUBE = "download_youtube"
    YOUTUBE_CACHE = "youtube_cache"
    FINAL_COMMON_MEDIA = "final_common_media"
    ERRORS = "errors"
    SAVE_YOUTUBE = "save_youtube"
