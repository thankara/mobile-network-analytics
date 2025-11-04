from pydantic import BaseModel


class TrafficRecord(BaseModel):
    """
    Schema for traffic record data.
    """

    interval_start_timestamp: str
    interval_end_timestamp: str
    msisdn: int
    bytes_uplink: int
    bytes_downlink: int
    service_id: int
    cell_id: int
