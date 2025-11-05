from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from mobile_network_analytics.api.repositories.kpi_repositories import CellsKPIRepository, ServicesKPIRepository
from mobile_network_analytics.db.db import get_db_session
from mobile_network_analytics.schemas.utils import Interval


class ServicesKPIService:

    def __init__(self, service_kpi_repository: ServicesKPIRepository):
        self.service_kpi_repository = service_kpi_repository

    def get_service_kpi_data(
        self,
        interval: Interval,
        interval_start_timestamp: str | None = None,
        interval_end_timestamp: str | None = None,
        service_id: int | None = None
    ) -> list:
        return self.service_kpi_repository.get_service_kpi_data(
            interval=interval,
            interval_start_timestamp=interval_start_timestamp,
            interval_end_timestamp=interval_end_timestamp,
            service_id=service_id
        )


class CellsKPIService:

    def __init__(self, cell_kpi_repository: CellsKPIRepository):
        self.cell_kpi_repository = cell_kpi_repository

    def get_cell_kpi_data(
        self,
        interval: Interval,
        interval_start_timestamp: str | None = None,
        interval_end_timestamp: str | None = None,
        cell_id: int | None = None
    ) -> list:
        return self.cell_kpi_repository.get_cell_kpi_data(
            interval=interval,
            interval_start_timestamp=interval_start_timestamp,
            interval_end_timestamp=interval_end_timestamp,
            cell_id=cell_id
        )


def get_services_kpi_service(session: Annotated[Session, Depends(get_db_session)]) -> ServicesKPIService:
    service_kpi_repository = ServicesKPIRepository(session=session)
    return ServicesKPIService(service_kpi_repository=service_kpi_repository)


def get_cells_kpi_service(session: Annotated[Session, Depends(get_db_session)]) -> CellsKPIService:
    cell_kpi_repository = CellsKPIRepository(session=session)
    return CellsKPIService(cell_kpi_repository=cell_kpi_repository)
