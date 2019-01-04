import os
from datetime import datetime, timedelta


def get_output_path(fn):
    out_dir = os.path.join(os.path.dirname(__file__), 'output')
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    return os.path.join(out_dir, fn)


def datetime_range(start: datetime = None, end: datetime = None, delta: timedelta = None):
    if isinstance(start, datetime) \
            and isinstance(end, datetime) \
            and isinstance(delta, timedelta):
        while start <= end:
            yield start
            start += delta
