from enum import Enum


class Interval(str, Enum):
    FIVE_MINUTE = "5-minute"
    ONE_HOUR = "1-hour"
