import os
from datetime import datetime, timedelta

from mobile_network_analytics.schemas.utils import Interval


def extract_timestamp_from_filename(filename: str) -> datetime:
    """
    Extracts the interval_end_timestamp (in ms) from filenames formatted like:
    ipflow_data.ts-1488355500000.1.csv
    """
    try:
        parts = filename.split(".")
        ts_part = parts[1]
        return int(ts_part.split("-")[1])
    except (IndexError, ValueError):
        return None


def get_time_window(interval: Interval, end_time: datetime) -> tuple[int, int]:
    """
    Given an interval and an end_time, returns the corresponding start_time and end_time
    as a tuple of UNIX timestamps in milliseconds.
    """
    if interval == Interval.FIVE_MINUTE:
        delta = timedelta(minutes=5)
    elif interval == Interval.ONE_HOUR:
        delta = timedelta(hours=1)
    else:
        raise ValueError(f"Unsupported interval: {interval}")

    start_time = end_time - delta

    # Convert to UNIX timestamps in milliseconds
    start_ts = int(start_time.timestamp() * 1000)
    end_ts = int(end_time.timestamp() * 1000)

    return start_ts, end_ts


def get_interval_files(directory_path: str, start_ts: int, end_ts: int) -> list[str]:
    """
    Return all files with interval_end_timestamp between start_ts and end_ts.
    """
    matching_files = []
    for file in os.listdir(directory_path):
        ts = extract_timestamp_from_filename(file)
        if ts is not None and start_ts <= ts <= end_ts:
            matching_files.append(os.path.join(directory_path, file))

    return matching_files
