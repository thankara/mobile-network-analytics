from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from mobile_network_analytics.db import Base
from mobile_network_analytics.schemas.utils import Interval


class DBServiceData(Base):
    __tablename__ = "service_data"

    id: Mapped[int] = mapped_column(primary_key=True, init=False, autoincrement=True)
    interval_start_timestamp: Mapped[str] = mapped_column(String(30), nullable=False, init=True)
    interval_end_timestamp: Mapped[str] = mapped_column(String(30), nullable=False, init=True)
    service_id: Mapped[int] = mapped_column(nullable=False, init=True)
    total_bytes: Mapped[int] = mapped_column(nullable=False, init=True)
    interval: Mapped[Interval] = mapped_column(nullable=False, init=True)
