from pydantic import BaseModel

from mobile_network_analytics.schemas.utils import Interval


class CellData(BaseModel):
    """
    Schema for cell data.
    """

    interval_start_timestamp: str
    interval_end_timestamp: str
    cell_id: int
    number_of_unique_users: int
    interval: Interval
