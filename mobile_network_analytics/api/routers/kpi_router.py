from typing_extensions import Annotated
from fastapi import APIRouter, Depends

from mobile_network_analytics.api.services.kpi_services import CellsKPIService, ServicesKPIService, get_cells_kpi_service, get_services_kpi_service
from mobile_network_analytics.schemas.cell_data import CellData
from mobile_network_analytics.schemas.service_data import ServiceData
from mobile_network_analytics.schemas.utils import Interval

kpi_router = APIRouter(prefix="/kpi", tags=["KPI"])


@kpi_router.get("/services", response_model=list[ServiceData])
def get_service_kpi(
    services_kpi_service: Annotated[ServicesKPIService, Depends(get_services_kpi_service)],
    interval: Interval = Interval.FIVE_MINUTE,
    interval_start_timestamp: str | None = None,
    interval_end_timestamp: str | None = None,
    service_id: int | None = None
):
    return services_kpi_service.get_service_kpi_data(
        interval=interval,
        interval_start_timestamp=interval_start_timestamp,
        interval_end_timestamp=interval_end_timestamp,
        service_id=service_id
    )


@kpi_router.get("/cells", response_model=list[CellData])
def get_cell_kpi(
    cells_kpi_service: Annotated[CellsKPIService, Depends(get_cells_kpi_service)],
    interval: Interval = Interval.FIVE_MINUTE,
    interval_start_timestamp: str | None = None,
    interval_end_timestamp: str | None = None,
    cell_id: int | None = None
):
    return cells_kpi_service.get_cell_kpi_data(
        interval=interval,
        interval_start_timestamp=interval_start_timestamp,
        interval_end_timestamp=interval_end_timestamp,
        cell_id=cell_id
    )
