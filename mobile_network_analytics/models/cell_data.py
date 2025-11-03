from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from mobile_network_analytics.db import Base
from mobile_network_analytics.schemas.utils import Interval


class CellData(Base):
    __tablename__ = "cell_data"

    id: Mapped[int] = mapped_column(primary_key=True, init=False, autoincrement=True)
    interval_start_timestamp: Mapped[datetime] = mapped_column(nullable=False, init=True)
    interval_end_timestamp: Mapped[datetime] = mapped_column(nullable=False, init=True)
    cell_id: Mapped[int] = mapped_column(nullable=False, init=True)
    number_of_unique_users: Mapped[int] = mapped_column(nullable=False, init=True)
    interval: Mapped[Interval] = mapped_column(nullable=False, init=True)
