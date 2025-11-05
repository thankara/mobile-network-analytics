from datetime import datetime

from mobile_network_analytics.schemas.utils import Interval
from mobile_network_analytics.data_ingestion.file_extraction_utils import get_time_window


def test_get_time_window():
    start_ts, end_ts = get_time_window(Interval.FIVE_MINUTE, datetime(2023, 1, 1, 12, 0, 0))
    assert start_ts == 1672566900000  # 2023-01-01 11:55:00 in ms
    assert end_ts == 1672567200000    # 2023-01-01 12:00:00 in ms


def test_get_time_window_one_hour():
    start_ts, end_ts = get_time_window(Interval.ONE_HOUR, datetime(2023, 1, 1, 12, 0, 0))
    assert start_ts == 1672563600000  # 2023-01-01 11:00:00 in ms
    assert end_ts == 1672567200000    # 2023-01-01 12:00:00 in ms
