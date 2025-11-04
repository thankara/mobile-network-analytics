from annotated_types import Interval
from sqlalchemy import select
from sqlalchemy.orm import Session

from mobile_network_analytics.models.cell_data import DBCellData
from mobile_network_analytics.models.service_data import DBServiceData


class KPIRepository:

    def __init__(self, session: Session):
        self._session = session


class ServicesKPIRepository(KPIRepository):

    def get_service_kpi_data(
            self,
            interval: Interval,
            interval_start_timestamp: str | None = None,
            interval_end_timestamp: str | None = None,
            service_id: int | None = None
    ) -> list[DBServiceData]:
        query = select(DBServiceData).where(DBServiceData.interval == interval.value)

        if interval_start_timestamp:
            query = query.where(
                DBServiceData.interval_start_timestamp >= interval_start_timestamp
            )

        if interval_end_timestamp:
            query = query.where(
                DBServiceData.interval_end_timestamp <= interval_end_timestamp
            )

        if service_id:
            query = query.where(
                DBServiceData.service_id == service_id
            )

        return self._session.scalars(query).all()  # Can use pagination here if data is too large


class CellsKPIRepository(KPIRepository):

    def get_cell_kpi_data(
            self,
            interval: Interval,
            interval_start_timestamp: str | None = None,
            interval_end_timestamp: str | None = None,
            cell_id: int | None = None
    ) -> list[DBCellData]:
        query = select(DBCellData).where(DBCellData.interval == interval.value)

        if interval_start_timestamp:
            query = query.where(
                DBCellData.interval_start_timestamp >= interval_start_timestamp
            )

        if interval_end_timestamp:
            query = query.where(
                DBCellData.interval_end_timestamp <= interval_end_timestamp
            )

        if cell_id:
            query = query.where(
                DBCellData.cell_id == cell_id
            )

        return self._session.scalars(query).all()  # Can use pagination here if data is too large
