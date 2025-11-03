from datetime import datetime
from pydantic import BaseModel

from mobile_network_analytics.schemas.utils import Interval


class ServiceData(BaseModel):
    """
    Schema for service data.
    """

    interval_start_timestamp: datetime
    interval_end_timestamp: datetime
    service_id: int
    total_bytes: int
    interval: Interval
