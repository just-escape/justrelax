import os

from justrelax.common.utils import human_readable_size
from justrelax.orchestrator import conf


class MediaManager:
    @staticmethod
    def get_all():
        files = []
        for f in os.listdir(conf.MEDIA_DIRECTORY):
            f_path = os.path.join(conf.MEDIA_DIRECTORY, f)
            if os.path.isfile(f_path):
                stat = os.stat(f_path)
                file_data = {
                    'name': f,
                    'date': stat.st_mtime,
                    'size': human_readable_size(stat.st_size),
                }
                files.append(file_data)
        return files
